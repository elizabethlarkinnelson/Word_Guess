from django.db import models

# Create your models here.


class Word(models.Model):

    current_word = models.CharField(max_length=11)
    guess_number = models.IntegerField()
    letters_left = models.CharField(max_length=11)
