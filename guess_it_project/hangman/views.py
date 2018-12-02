from django.shortcuts import render
from .models import Word
import requests
import random


def index(request):
    return render(request, 'hangman/index.html')


def play(request):

    response = requests.get('http://app.linkedin-reach.io/words?minLength=3&maxLength=10')
    words = response.text.splitlines()

    random_num = random.randint(0, len(words))
    word = words[random_num]
    length = [i for i in range(len(word))]

    new_word = Word(current_word=word, guess_number=0, letters_left=''.join(sorted(word)))
    new_word.save()

    context = {'length': length}

    return render(request, 'hangman/play.html', context)


def game(request):

    context = {}
    success = 'success'

    if request.method == 'POST':
        guess = request.POST['guess']
        context = {'success': success}

    return render(request, 'hangman/game.html', context)
