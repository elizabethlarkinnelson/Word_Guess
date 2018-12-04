from django.shortcuts import render
from .models import Word
import requests
import random


def index(request):
    return render(request, 'hangman/index.html')


def difficulty(request):
    return render(request, 'hangman/difficulty.html')


def play(request):

    if request.method == 'POST':
        difficulty = request.POST['difficulty']

    response = requests.get('http://app.linkedin-reach.io/words?difficulty='
                            + str(difficulty) + '&minLength=3&maxLength=6')
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
        if 'guess' in request.POST:
            guess = request.POST['guess']
            if guess.isalpha():
                current_word.guess_number += 1
                current_word.save()

                if guess in current_word.letters_left and current_word.guess_number < 6:
                    current_word.right_letters_guessed = current_word.right_letters_guessed + guess
                    current_word.save()
                    letters_left = []
                    for let in current_word.letters_left:
                        if let == guess:
                            pass
                        else:
                            letters_left.append(let)
                    letters_left_string = ''.join(letters_left)
                    current_word.letters_left = letters_left_string
                    current_word.save()

                    context['right_letters'] = current_word.right_letters_guessed
                    context['letters_left'] = current_word.letters_left
                    context['wrong_guess'] = len(current_word.wrong_letters_guessed)

                    if current_word.letters_left == '':
                        return render(request, 'hangman/won.html', context)

                elif guess in current_word.letters_left and current_word.guess_number == 6:
                    if current_word.letters_left == guess:
                        return render(request, 'hangman/won.html', context)

                elif guess not in current_word.letters_left and current_word.guess_number > 5:
                    return render(request, 'hangman/loss.html', context)

                elif guess not in current_word.letters_left and current_word.guess_number == 6:
                    return render(request, 'hangman/loss.html', context)

                else:
                    current_word.wrong_letters_guessed = current_word.wrong_letters_guessed + guess
                    current_word.save()
                    if current_word.wrong_words_guessed:
                        context['wrong_guess'] = len(current_word.wrong_letters_guessed) + current_word.wrong_words_guessed.count('/')
                    else:
                        context['wrong_guess'] = len(current_word.wrong_letters_guessed)
            else:
                context = {'error': error}

        else:
            word_guess = request.POST['word_guess']
            current_word.guess_number += 1
            current_word.save()
            if word_guess.strip() == current_word.current_word and current_word.guess_number < 7:
                return render(request, 'hangman/won.html', context)
            elif word_guess.strip() != current_word.current_word and current_word.guess_number < 6:
                if current_word.wrong_words_guessed:
                    current_word.wrong_words_guessed = current_word.wrong_words_guessed + word_guess + '/'
                    current_word.save()
                else:
                    current_word.wrong_words_guessed = word_guess + '/'
                    current_word.save()
                context['wrong_guess'] = len(current_word.wrong_letters_guessed) + current_word.wrong_words_guessed.count('/')
            elif word_guess.strip() != current_word.current_word and current_word.guess_number == 6:
                    return render(request, 'hangman/loss.html', context)

    context['guesses'] = current_word.guess_number
    context['guesses_left'] = 6 - context['guesses']

    if current_word.wrong_letters_guessed:
        context['wrong_letters_guessed'] = current_word.wrong_letters_guessed

    if current_word.wrong_words_guessed:
        each_wrong_word = []
        wrong_word = ''

        for char in current_word.wrong_words_guessed:
            if char != '/':
                wrong_word = wrong_word + char
            else:
                each_wrong_word.append(wrong_word)
                wrong_word = ''

        context['wrong_words_guessed'] = each_wrong_word

    word_guess = []

    for let in current_word.current_word:
        if let in current_word.right_letters_guessed:
            word_guess.append(let)
        else:
            word_guess.append('_')
    context['word_guess'] = word_guess

    return render(request, 'hangman/game.html', context)
