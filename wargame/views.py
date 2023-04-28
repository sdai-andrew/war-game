import json
from django.http import HttpResponse
from django.shortcuts import render
from wargame.forms import StartGameForm, LoginForm, RegisterForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.urls import reverse
from django.shortcuts import render, redirect
from wargame.models import Player
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from wargame.game import *

def play_game(request, p1name, p2name):
    if not request.user.is_authenticated:
        return _my_json_error_response("You must be logged in to do this operation", status=401)
    if request.method != 'POST':
        return _my_json_error_response("You must use a POST request for this operation", status=405)
    try:
        player1User = User.objects.get(username=p1name)
        player1 = player1User.player
        player2User = User.objects.get(username=p2name)
        player2 = player2User.player
    except ObjectDoesNotExist:
        return _my_json_error_response("Invalid.", status=400)
    game = Game()
    moves = game.play(False)
    lastMove = moves[-1]
    if not moves or not lastMove:
        return _my_json_error_response("Game Broke.", status=500)
    lastStatus = lastMove["status"]
    if lastStatus == "Player 1 won!":
        player1.wins += 1
        player1.save()
    elif lastStatus == "Player 2 won!":
        player2.wins += 1
        player2.save()
    else:
        print("FREAKING ERROR")
        return _my_json_error_response("Game Broke.", status=500)
    response_json = json.dumps({"moves": moves})
    return HttpResponse(response_json, content_type='application/json')


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
    context = {}
    if request.method != "POST":
        return redirect(reverse('home'))
    try:
        request.user.player
    except ObjectDoesNotExist:
        player = Player(user=request.user)
        player.save()
    form = StartGameForm(request.POST)
    if not form.is_valid():
        context = {}
        context["form"] = form
        return render(request, 'wargame/home.html', context)
    opponentName = form.cleaned_data["opponentName"]
    try:
        oppUser = User.objects.get(username=opponentName)
        opponent = oppUser.player
    except ObjectDoesNotExist:
        form.add_error('opponentName', 'User with that name does not exist')
        context["form"] = form
        return render(request, 'wargame/home.html', context)
    if oppUser.username == request.user.username:
        form.add_error('opponentName', "Can't war against yourself!")
        context["form"] = form
        return render(request, 'wargame/home.html', context)
    context["player1"] = request.user.username
    context["player2"] = opponent.user.username
    return render(request, 'wargame/game.html', context)

def get_wins_json(request, name):
    if not request.user.is_authenticated:
        return _my_json_error_response("You must be logged in to do this operation", status=401)
    response_data = {
        "player_exists": "true",
    }
    try:
        playerUser = User.objects.get(username=name)
        player = playerUser.player
    except ObjectDoesNotExist:
        response_data["player_exists"] = "false"
    response_data["player_name"] = name
    if response_data["player_exists"] == "true":
        response_data["wins"] = player.wins
    response_json = json.dumps(response_data)
    return HttpResponse(response_json, content_type='application/json')

def _my_json_error_response(message, status=200):
    response_json = '{"error": "' + message + '"}'
    return HttpResponse(response_json, content_type='application/json', status=status)

def login_action(request):
    context = {}
    if request.method == 'GET':
        context['form'] = LoginForm()
        return render(request, 'wargame/login.html', context)
    form = LoginForm(request.POST)
    context['form'] = form
    if not form.is_valid():
        return render(request, 'wargame/login.html', context)
    user = authenticate(username=form.cleaned_data['username'],
                        password=form.cleaned_data['password'])
    login(request, user)
    return redirect(reverse('home'))

def logout_action(request):
    logout(request)
    return redirect(reverse('login'))

@transaction.atomic
def register_action(request):
    context = {}
    if request.method == 'GET':
        context['form'] = RegisterForm()
        return render(request, 'wargame/registration.html', context)
    form = RegisterForm(request.POST)
    context['form'] = form
    if not form.is_valid():
        return render(request, 'wargame/registration.html', context)
    user = User.objects.create_user(username=form.cleaned_data['username'], 
                                    password=form.cleaned_data['password'])
    user.save()
    user = authenticate(username=form.cleaned_data['username'],
                        password=form.cleaned_data['password'])
    player = Player(user=user)
    player.save()

    login(request, user)
    return redirect(reverse('home'))