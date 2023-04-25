from django.shortcuts import render

def home_action(request):
    return render(request, 'wargame/home.html')
