from django.shortcuts import render


def index(request):
    return render(request, 'hangman/index.html')


def play(request):
    return render(request, 'hangman/play.html')
