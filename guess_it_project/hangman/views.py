from django.http import HttpResponse


def index(request):
    return HttpResponse("I'm in my project! Yipee!!")
