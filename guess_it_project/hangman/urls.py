from django.urls import path
from . import views

app_name = 'hangman'

urlpatterns = [
    path('', views.index, name='index'),
    path('play/', views.play, name='play'),
    path('game/', views.game, name='game'),
    path('difficulty/', views.difficulty,  name='difficulty'),
]
