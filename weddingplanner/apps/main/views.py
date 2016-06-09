from django.shortcuts import render, redirect


# the rewritten view!
def index(request):
    return render(request, 'index.html')
