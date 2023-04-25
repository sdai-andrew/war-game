from django import forms

class StartGameForm(forms.Form):
    player1Name = forms.CharField(max_length=25, widget=forms.TextInput(attrs={'placeholder': 'Player 1 Name'}))
    player2Name = forms.CharField(max_length=25, widget=forms.TextInput(attrs={'placeholder': 'Player 2 Name'}))