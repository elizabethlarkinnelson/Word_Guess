from django.db import models

# Create your models here.


class User(models.Model):
    question_text = models.CharField(max_length=200)
