# Generic tools, move this into a separate lib, later opensource
import contextlib
from functools import wraps, update_wrapper
import datetime
import shutil
from enum import Enum
import re
import os
from tempfile import NamedTemporaryFile
from fabric.context_managers import settings, lcd, cd, hide
from fabric.decorators import task
from fabric.operations import local, run, put
from fabric.state import env
from fabric.tasks import execute, WrappedCallableTask
from formic import formic

DEFAULT_TARGET_PARAM = 'target'

CONFIG = {
    'DEFAULT': {
        # Not used yet
        'version_file': 'VERSION',
        'timestamp_format': '%Y-%m-%d-%H-%M-%S',
        'service_name': 'weddingplanner'
    },
    'test': {
        'env_name': 'test',
        'hosts': ['root@']
    },
    'staging': {
        'hosts': ['root@'],
        'dest': '/usr/local/lib/weddingplanner/',
        'env_name': 'staging',
        'requirements': 'deployment',
        'static': '/var/www/weddingplanner'
    },
    'live': {
        'hosts': ['root@'],
        'dest': '/usr/local/lib/weddingplanner/',
        'env_name': 'deployment',
        'requirements': 'deployment',
        'static': '/var/www/weddingplanner'
    },
}

_TASKS_EXECUTED = set()

def config_for_target(target):
    config = CONFIG['DEFAULT']
    config.update(CONFIG[target])
    return config

# TODO: add default target
def configure(func,target_param=DEFAULT_TARGET_PARAM):
    # TODO: (when making a lib) could be imported from six as well
    def decorator(*args, **kwargs):
        if env.has_key('target_env'):
            execute(func, *args, **kwargs)
        else:
            target = kwargs.pop(target_param)
            config = config_for_target(target)
            config['target_env'] = target

            with settings(**config):
                execute(func, *args, **kwargs)

    return WrappedCallableTask(update_wrapper(decorator, func))

def depends(deps):
    def inner(func):
        func.deps = deps
        def decorator(*args, **kwargs):
            for dependency in func.deps:
                if not dependency in _TASKS_EXECUTED:
                    _TASKS_EXECUTED.add(dependency)
                    dependency(*args, **kwargs)
            return func(*args, **kwargs)

        return WrappedCallableTask(update_wrapper(decorator, func))
    return inner

@contextlib.contextmanager
def noop_context():
    yield

class FileMapping(object):
    """Mapping file parser for FileInstaller.
    The map file can use templating (jinja2). Templates will be evaluated before the
    actual parsing. Lines starting with # are treated as comments (and thus ignored).

    TODO: maybe use formic patterns?
    """
    class Entry(object):
        """A single entry describing the mapping for a single file.

        An entry looks like this:
        * simple file installation:
        <local_path> -> <remote_path> [<remote_mode>[,<remote_owner>[.<remote_group>]]]

        * file installation with template rendering:
        <local_path> => <remote_path> [<remote_mode>[,<remote_owner>[.<remote_group>]]]

        * remote link creation
        <remote_path> ~> <remote_path>
        """
        TYPE = Enum('EntryType', 'copy template link')
        __TYPE_MAP = {'-': TYPE.copy, '=': TYPE.template, '~': TYPE.link}

        def __init__(self, source, dest, type, mode=None, owner=None,group=None):
            self.source = source
            self.dest = dest
            self.type = self.__TYPE_MAP[type]
            self.mode = mode
            self.owner = owner
            self.group = group

    COMMENT_RX = re.compile(r'^\s*#.*$')
    __NAME_RX = r'[a-z][-a-z0-9]*'
    ENTRY_PARSER_RX = re.compile(r'\s*(?P<source>[^ ]+)\s+(?P<type>[\-~=])>\s+(?P<dest>[^ ]+)'
        '(?:\s+(?P<mode>[0-7]4)(?:,(?P<owner>{name_rx})?(?:\.(?P<group>{name_rx}))?)?)?\s*$'
                                 .format(name_rx = __NAME_RX))

    def __init__(self, mapping_file):
        """
        @param mapping_file: Mapping file to read mapping from. (Either the file name or a
        'file-like' object having a readlines() method.)
        @type mapping_file: basestring|file
        """
        if isinstance(mapping_file, basestring):
            with open(mapping_file) as f:
                self.__parse(f)
        else:
            self.__parse(mapping_file)

    def __parse(self, map):
        self.entries = []

        for cnt, line in enumerate(map.readlines()):
            if not self.COMMENT_RX.match(line):
                values = self.ENTRY_PARSER_RX.match(line.strip())

                if values:
                    self.entries.append(self.Entry(**values.groupdict()))
                else:
                    raise ValueError('Syntax error on line %d: %s' % (cnt, line))

class FileInstaller(object):
    """Install files using a map file."""
    # python stupidity... see real definition at the end of the class
    _TYPE_HANDLERS = {}

    @classmethod
    def install(cls, mapping, base_dir=None, dest_dir='.', context={}):
        """Install files as described by the specified mapping. At least one of base_dir or
        dest_dir should be specified.

        NOTE: ownership parameters are currently ignored.

        @param mapping: Parsed mapping
        @type mapping: FileMapping
        @param base_dir: the base directory which is used for interpreting relative paths in the
        mapping.
        @type base_dir: basestring
        @param dest_dir: the directory where the installation files go to. (All target paths are
          created under this directory.) dest_dir is either absolute or is interpreted as relative
          to base_dir.
        @type dest_dir: basestring
        @param context: context to use for
        @return: The list of files/links created (with paths relative to dest_dir)
        """
        result = []
        with lcd(base_dir) if base_dir else noop_context():
            for entry in mapping.entries:
                dest = os.path.join(dest_dir, entry.dest)
                if dest[:-1] == os.path.sep:
                    dest = os.path.join(dest, os.path.basename(entry.source))

                dest_file_dir = os.path.dirname(dest)
                local('mkdir -p %s' % dest_file_dir)
                cls._TYPE_HANDLERS[entry.type](entry.source, dest, context)
                if entry.mode:
                    # TODO: consider using shutils
                    local('chmod %s %s' % (entry.mode, dest))
                    # TODO: generate script to change ownership AND update the specified tar file,
                    # then run it under fakeroot (might work...)
                result.append(dest[len(dest_dir)+1:])

        return result

    @classmethod
    def copy_file(cls, source,dest, _):
        shutil.copy(source, dest)

    @classmethod
    def copy_template(cls, source, dest, context):
        from jinja2 import Environment, FileSystemLoader
        env = Environment(loader=FileSystemLoader('.'))
        with open(dest, 'w+') as out:
            out.write(env.get_template(source).render(context))

    @classmethod
    def create_link(cls, source, dest, _):
        local('ln -sfn %s %s' % (source, dest))

# Boy, is this lame...
FileInstaller._TYPE_HANDLERS = {
    FileMapping.Entry.TYPE.copy: FileInstaller.copy_file,
    FileMapping.Entry.TYPE.template: FileInstaller.copy_template,
    FileMapping.Entry.TYPE.link: FileInstaller.create_link,

}

def tar(files,file_name,update=False):
    """
    Create/update tar archive.
    """
    mode = 'r' if update else 'c'
    with NamedTemporaryFile(delete=False) as list_file:
        cwd = os.getcwd()
        list_file.write('\n'.join(f[len(cwd) + 1:] if f.startswith(cwd) else f for f in files))
        list_file.flush()
        local('tar {mode}f {arch_name} -T {list}'.format(
            mode=mode, arch_name=file_name, list=list_file.name
        ))
#
# Task definitions
#

@configure
@task
def build(patch=False):
    # TODO: use fakeroot when building the archive (if needed)
    local('rm -rf build/*')
    local('mkdir -p build')

    # Only files present in Git will be deployed
    # TODO: not used now!, move into a separate method, and ... <-> !!! may not work with locally
    #   built files, those will need to be added separately
    candidates = local('git ls-files', capture=True).stdout.split('\n')
    # TODO: for each local('git submodule --quiet foreach pwd') generate file list with the above

    app_files = formic.FileSet(
        include=[
            '/requirements/**', '/weddingplanner/**', '/static/**', '/templates/**', '/manage',
        ], exclude=[
            '/weddingplanner/settings/environment.py', '*.pyc'
        ]
    ) #, walk=formic.walk_from_list(candidates))

    # git filtering is disabled for now, as the front end is not part of this repo AND no way to find errors
    # caused by missing files without testing

    tar(app_files, 'build/deploy.tar')

    generated = FileInstaller.install(FileMapping('deploy.map'), dest_dir='build', context=env)

    # NOTE: in order to be able to build the virtualenv locally, we need an identical OS to the
    # deployment target. (As sad as it is with a 'cross platform' python env.) So we need to build
    # in a chroot/docker image. Use the -v option to mount the project directory: https://docs.docker.com/userguide/dockervolumes/

    #    local("""sudo docker run -v %s:/tmp/app_build --rm --user 1000 -w /tmp/app_build/build 3e5bc530829f /bin/bash -c "apt-get install -y python-dev libffi-dev ; virtualenv env ; env/bin/pip install -r ../requirements/deployment.txt" """ % os.getcwd())
    with lcd('build'):
        tar(generated, 'deploy.tar', update=True)
        # The below two lines don't work, because we're using a different OS on the server
        # local('virtualenv env')
        # local('env/bin/pip install -r ../requirements/%s.txt' % env.requirements)

        # NOTE: enable these, once virtualenv preparation works in docker
#        local('virtualenv --relocatable env')
#        local('tar rf deploy.tar env')

        # NOTE: better compression doesn't yield enough speedup on uploading to make up for the
        #  slower compressor run time
        local('gzip deploy.tar')

@configure
@depends([build])
@task
def deploy():
    timestamp = datetime.datetime.utcnow().strftime(env.timestamp_format)
    version = local('git rev-parse HEAD', capture=True).stdout.strip()
    run('mkdir -p %s' % env.dest)
    with cd(env.dest):
        run('mkdir %s' % timestamp)
        with cd(timestamp):
            remote_archive = '/tmp/weddingplanner-%s-%s.tar.gz' % (timestamp, version)
            # TODO: use rsync in a '3-way' mode (--link-dest) to minimize files transfered
            #  (do the same for the locally built virtualenv)
            put('build/deploy.tar.gz', remote_archive)
            # TODO: remove --no-same-owner when built with fakeroot
            run('tar xfz %s --no-same-owner' % remote_archive)

            with hide('stdout'):
                run('virtualenv env')

                # NOTE: Temporary solution: install through running pip remotely
                run('env/bin/pip install -r requirements/%s.txt' % env.requirements)
                # NOTE: take it from the settings...
                run('mkdir assets')
                # NOTE: can also be run locally
                run('env/bin/python manage collectstatic -v 0 -l --noinput -c')

            run('env/bin/python manage migrate')

        with settings(warn_only=True):
            result =  run('supervisorctl status | grep "%s\s\+RUNNING"' % env.service_name)

        if not result.failed:
            run('supervisorctl stop %s' % env.service_name)

        run('ln -sfn %s current' % timestamp)
        run('supervisorctl start %s' % env.service_name)


@configure
@depends([build])
@task
def test():
    print 'Test'

@task
def rebuild_db():
    """Drop and re-sync the app specific tables from the db, load dev fixtures"""
    local('bin/drop_model')
    local('./manage syncdb')
    local('./manage loaddata tests/fixtures.json')
