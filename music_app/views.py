from django.shortcuts import render

def index(request):
    """Home page for music app"""
    return render(request, 'music_app/index.html')
