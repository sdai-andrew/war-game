# Introduction
This is my implementation of a RESTful service that implements the card game War. Users can register and login to accounts and simulate the game against other users, as well as check how many wins a user has. The game is simulated entirely on the server and then rendered in the browser.
These are the specifications of War that were implemented:
- Each player starts with half a shuffled deck of 52 playing cards
- Ace is the high card and two is the low card
- Upon ties/war, each player places a face down card and then a face up card to determine the winner
- If a tir occurs and a player is out of cards, their last played card is the card used to determine the winner
- Ties/war can stack
- In the unlikely scenario that ties/wars occur continously to the point both players are out of cards, all cards are reshuffled and redistributed based on the number of cards each player had before the first tir/war occurred
- The winning cards of each hand are added to the winner's deck randomly to prevent infinite games
- The loser of the game is the one that exhausts their deck

# Technology
This service uses the Python framework Django and additionally utilizes AJAX. The main branch contains the code that runs the server on an AWS EC2 instance at http://3.136.19.125. To avoid bots that may scan for open ports and ruin me, I have disabled incoming traffic from all sources.
If you would like to test the deployment, feel free to email me at stephen6dai@gmail.com and I can allow traffic.
With the local branch, you can test the service locally. This will require use of [Django](https://www.djangoproject.com/) and creating a Django secret key to put in the config.ini file. First rename the *config.ini.sample* file to just *config.ini*. A Django secret key can be generated by running the following commands in a Python Shell:
```
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```
Copy the secret key and paste it into the *"Your secret here!"* in *config.ini*, and ensure you have double quotations around the secret key.
You can now run the server locally.

# Features
- User login and registration
- Endpoint to simulate War against another user
- Endpoint to get a user's number of wins
- Game page that renders one turn/move of the game per 1.5 seconds
- mySQL database and Apache HTTP server for deployment
- SQLite3 database for local

# If More Time
- Rendering a scrollable list to see all moves so you don't have to wait a while for a full game to complete
- Solving race conditions that occur when fetching a player and incrementing their wins (could be done with a @transaction.atomic decorator for play_game())
- Minimizing amount of data sent from server to clients; my implementation is correct but optimizations could be made to minimize packet size
- Better UI in general (making cards more card-like with their suits and values); opted to not have that great of a UI because it was not worth the time
- Being able to toggle the speed at which rendering occurs
