import random
from collections import deque

JACK = 10
QUEEN = 11
KING = 12
ACE = 13
HEARTS = "Hearts"
DIAMONDS = "Diamonds"
SPADES = "Spades"
CLOVERS = "Clovers"
VALUES = [i for i in range(1, ACE + 1)]
SUITS = [HEARTS, DIAMONDS, SPADES, CLOVERS]

class Game():
    @staticmethod
    def generateDeck():
        deck = []
        for suit in SUITS:
            for value in VALUES:
                deck.append(Card(suit, value))
        return deck

    def __init__(self):
        deck = Game.generateDeck()
        random.shuffle(deck)
        self.player1 = GamePlayer(deque(deck[:(len(deck) // 2)]))
        self.player2 = GamePlayer(deque(deck[(len(deck) // 2):]))
        self.moves = []
    
    def serializeMove(self, status, p1Card, p2Card, p1FaceUp, p2FaceUp):
        result = {}
        result["Status"] = status
        result["p1NumCards"] = len(self.player1.deck)
        result["p2NumCards"] = len(self.player2.deck)
        oneCard = {}
        if p1FaceUp == None:
            oneCard["isFaceUp"] = "None"
        elif p1FaceUp:
            oneCard["isFaceUp"] = "True"
            oneCard["Suit"] = p1Card.suit
            oneCard["Value"] = p1Card.value
        else: 
            oneCard["isFaceUp"] = "False"
        result["p1Card"] = oneCard
        twoCard = {}
        if p2FaceUp == None:
            twoCard["isFaceUp"] = "None"
        elif p2FaceUp:
            twoCard["isFaceUp"] = "True"
            twoCard["Suit"] = p2Card.suit
            twoCard["Value"] = p2Card.value
        else: 
            twoCard["isFaceUp"] = "False"
        result["p2Card"] = twoCard
        self.moves.append(result)


    def play(self):
        # add move to indicate start of game
        self.serializeMove("Starting Game", None, None, None, None)
        war = []
        while self.player1.deck and self.player2.deck:
            player1Card = self.player1.deck.popleft()
            player2Card = self.player2.deck.popleft()
            war.extend([player1Card, player2Card])
            if player1Card.value > player2Card.value:
                self.player1.deck.extend(war)
                self.serializeMove("Player 1 victory", player1Card, player2Card, True, True)
            elif player2Card.value > player1Card.value:
                self.player2.deck.extend(war)
                self.serializeMove("Player 2 victory", player1Card, player2Card, True, True)
            else:
                self.serializeMove("Tie, time for war!", player1Card, player2Card, True, True)
                isWar = True
                while isWar:
                    # add face down cards
                    self.serializeMove("Tie, time for war!", None, None,
                                       None if len(self.player1.deck) == 0 else False,
                                       None if len(self.player1.deck) == 0 else False)
                    if self.player1.deck:
                        war.append(self.player2.deck.popleft())
                    if self.player2.deck:
                        war.append(self.player2.deck.popleft())
                    # add face up cards
                    if self.player1.deck:
                        player1Card = self.player2.deck.popleft()
                    if self.player2.deck:
                        player2Card = self.player2.deck.popleft()
                    war.extend([player1Card, player2Card])
                    status = ""
                    if player1Card.value > player2Card.value:
                        self.player1.deck.extend(war)
                        status = "Player 1 victory"
                        isWar = False
                    elif player2Card.value > player1Card.value:
                        self.player2.deck.extend(war)
                        status = "Player 2 victory"
                        isWar = False
                    else:
                        status = "Tie again, time for war!"
                    self.serializeMove(status, player1Card, player2Card, True, True)
        status = "Player 1 won!" if len(self.player2.deck) == 0 else "Player 2 won!"
        self.serializeMove(status, None, None, None, None)
        return self.moves            

class Card():
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value
    
    def __eq__(self, other):
        return (isinstance(other, self.__class__) and other.suit == self.suit and
                other.value == self.value)

    def __hash__(self):
        return hash(self.suit + str(self.value))

class GamePlayer():
    def __init__(self, deck):
        self.deck = deck
    