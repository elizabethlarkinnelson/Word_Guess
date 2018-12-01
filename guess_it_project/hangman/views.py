from django.shortcuts import render
import requests
import random


def index(request):
    response = requests.get('http://app.linkedin-reach.io/words?minLength=3&maxLength=10')
    words = response.text.splitlines()

    length = len(words)
    random_num = random.randint(0, length)

    word = words[random_num]
    context = {'word': word}
    return render(request, 'hangman/index.html', context)


def play(request):

    return render(request, 'hangman/play.html')
