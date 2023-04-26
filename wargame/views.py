import json
from django.http import HttpResponse
from django.shortcuts import render
from wargame.forms import StartGameForm
from django.urls import reverse
from django.shortcuts import render, redirect
from wargame.models import Player
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from wargame.game import *

def home_action(request):
    context = {}
    context["form"] = StartGameForm()
    return render(request, 'wargame/home.html', context)

def go_game(request):
    if request.method != "POST":
        return redirect(reverse('home'))
    form = StartGameForm(request.POST)
    if not form.is_valid:
        context = {}
        context["form"] = StartGameForm()
        return render(request, 'wargame/home.html', context)
    p1Name = form.cleaned_data["player1Name"]
    p2Name = form.cleaned_data["player2Name"]
    try:
        player1 = Player.objects.get(name=p1Name)
    except MultipleObjectsReturned:
        print("Multiple player 1's detected for name " + p1Name)
        player1 = Player.objects.filter(name=p1Name).first()
    except ObjectDoesNotExist:
        player1 = Player(name=p1Name)
        player1.save()
    try:
        player2 = Player.objects.get(name=p2Name)
    except MultipleObjectsReturned:
        print("Multiple player 2's detected for name " + p2Name)
        player2 = Player.objects.filter(name=p2Name).first()
    except ObjectDoesNotExist:
        player2 = Player(name=p1Name)
        player2.save()
    return render(request, 'wargame/game.html')

def get_wins_json(request, name):
    try:
        player = Player.objects.get(name=name)
    except MultipleObjectsReturned:
        print("Multiple player 1's detected for name " + name)
        player = Player.objects.filter(name=name).first()
    except ObjectDoesNotExist:
        player = Player(name=name)
        player.save()
    response_data = {
        "player_name": name,
        "wins": player.wins,
    }
    response_json = json.dumps(response_data)
    return HttpResponse(response_json, content_type='application/json')
