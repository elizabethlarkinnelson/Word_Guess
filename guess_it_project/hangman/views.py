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

    new_word = Word(current_word=word, guess_number=0,
                    letters_left=''.join(sorted(word)),
                    wrong_letters_guessed='',
                    right_letters_guessed='')
    new_word.save()

    context = {'length': length,
               'word': word}

    return render(request, 'hangman/play.html', context)


def game(request):

    context = {}
    error = 'invalid input'

    current_word = Word.objects.latest('id')

    if request.method == 'POST':
        guess = request.POST['guess']
        if guess.isalpha():
            current_word.guess_number += 1
            current_word.save()

            if guess in current_word.letters_left:
                current_word.right_letters_guessed = current_word.right_letters_guessed + guess
                current_word.save()
                letters_left = []
                count = 0
                for let in current_word.letters_left:
                    if let == guess and count == 0:
                        count += 1
                        pass
                    else:
                        letters_left.append(let)
                letters_left_string = ''.join(letters_left)
                current_word.letters_left = letters_left_string
                current_word.save()

                context['right_letters'] = current_word.right_letters_guessed
                context['letters_left'] = current_word.letters_left

            else:
                current_word.wrong_letters_guessed = current_word.wrong_letters_guessed + guess
        else:
            context = {'error': error}

    context['guesses'] = current_word.guess_number
    context['guesses_left'] = 6 - context['guesses']
    context['word'] = current_word.current_word
    context['length'] = [i for i in range(len(context['word']))]

    return render(request, 'hangman/game.html', context)
