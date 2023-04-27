import json
from django.http import HttpResponse
from django.shortcuts import render
from wargame.forms import StartGameForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse
from django.shortcuts import render, redirect
from wargame.models import Player
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from wargame.game import *

@login_required
def home_action(request):
    try:
        request.user.player
    except ObjectDoesNotExist:
        player = Player(user=request.user)
        player.save()
    context = {}
    context["form"] = StartGameForm()
    return render(request, 'wargame/home.html', context)

@login_required
def go_game(request):
    if request.method != "POST":
        return redirect(reverse('home'))
    try:
        request.user.player
    except ObjectDoesNotExist:
        player = Player(user=request.user)
        player.save()
    form = StartGameForm(request.POST)
    if not form.is_valid:
        context = {}
        context["form"] = form
        return render(request, 'wargame/home.html', context)
    opponentName = form.cleaned_data["opponentName"]
    try:
        oppUser = User.objects.get(username=opponentName)
        opponent = oppUser.player
    except MultipleObjectsReturned:
        # for debugging sake, should never happen
        print("Multiple player 1's detected for name " + opponentName)
        oppUser = User.objects.filter(username=opponentName).first()
        opponent = oppUser.player
    except ObjectDoesNotExist:
        context= {}
        form.add_error('opponentName', 'User with that name does not exist')
        context["form"] = form
        return render(request, 'wargame/home.html', context)
    
    context = {}
    context["player1"] = request.user.username
    context["player2"] = opponent.user.username
    return render(request, 'wargame/game.html', context)

def get_wins_json(request, name):
    if not request.user.is_authenticated:
        return _my_json_error_response("You must be logged in to do this operation", status=401)
    response_data = {
        "exists": "true",
    }
    try:
        playerUser = User.objects.get(username=name)
        player = playerUser.player
    except MultipleObjectsReturned:
        # for debugging sake, should never happen
        print("Multiple player 1's detected for name " + name)
        playerUser = User.objects.filter(username=name).first()
        player = playerUser.player
    except ObjectDoesNotExist:
        response_data["exists"] = "false"
    response_data["player_name"] = name
    response_data["wins"] = player.wins
    response_json = json.dumps(response_data)
    return HttpResponse(response_json, content_type='application/json')

def _my_json_error_response(message, status=200):
    response_json = '{"error": "' + message + '"}'
    return HttpResponse(response_json, content_type='application/json', status=status)