from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

class StartGameForm(forms.Form):
    player1Name = forms.CharField(max_length=25, widget=forms.TextInput(attrs={'placeholder': 'Player 1 Name'}))
    player2Name = forms.CharField(max_length=25, widget=forms.TextInput(attrs={'placeholder': 'Player 2 Name'}))

class LoginForm(forms.Form):
    username = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(max_length=200, widget=forms.PasswordInput(attrs={"placeholder": "Password"}))

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError("Invalid username/password")
        return cleaned_data
    
class RegisterForm(forms.Form):
    username   = forms.CharField(max_length=20, widget=forms.TextInput(attrs={"placeholder": "Username"}))
    password  = forms.CharField(max_length=200,
                                 label='Password', 
                                 widget=forms.PasswordInput(attrs={"placeholder": "Password"}))
    confirm_password  = forms.CharField(max_length=200,
                                 label='Confirm',  
                                 widget=forms.PasswordInput(attrs={"placeholder": "Confirm Password"}))

    def clean(self):
        cleaned_data = super().clean()

        # Confirms that the two password fields match
        password1 = cleaned_data.get('password')
        password2 = cleaned_data.get('confirm_password')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match.")
        return cleaned_data

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username is already taken.")
        return username