"""
Settings for weddingplanner

Settings for different environments are stored in separate files (modules).

.base (base.py) is always loaded first then the setting for the selected environment is
loaded. Environment specific settings can thus reference the values from .base

Environment selection is done in .environment.ENVIRONMENT (environment.py).
"""

import __builtin__
from .base import *
from . import environment

__imported_module = __builtin__.__import__('%s' % environment.ENVIRONMENT, globals(), locals(), ['*'], -1)
locals().update(__imported_module.__dict__)
