from django.shortcuts import render
from wargame.forms import StartGameForm

def home_action(request):
    context = {}
    context["form"] = StartGameForm()
    return render(request, 'wargame/home.html')

