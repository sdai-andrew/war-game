import unittest
from django.test import TestCase
from wargame.models import Player
from wargame.game import *


class PlayerTestCase(TestCase):
    def setUp(self):
        Player.objects.create(name="Player A")
        Player.objects.create(name="Player B")
    
class GameTest(TestCase):
    def test_deck_creation(self):
        deck = Game.generateDeck()
        for card in deck:
            self.assertIsInstance(card, Card)
            self.assertIsNotNone(card)
            self.assertIn(card.value, VALUES)
            self.assertIn(card.suit, SUITS)
        self.assertEqual(len(deck), 52)
        deckSet = set(deck)
        self.assertEqual(len(deck), len(deckSet))
    
    def test_game_creation(self):
        game = Game()
        self.assertEqual(game.moves, [])
        self.assertEqual(len(game.player1.deck), 26)
        self.assertEqual(len(game.player2.deck), 26)
        for card in game.player1.deck:
            self.assertNotIn(card, game.player2.deck)
        for card in game.player2.deck:
            self.assertNotIn(card, game.player1.deck)
    
    def test_serialize_move(self):
        game = Game()
        p1TestCard = Card(SPADES, JACK)
        p2TestCard = Card(DIAMONDS, 3)
        game.player1.deck = deque([p1TestCard])
        game.player2.deck = deque([p2TestCard])
        game.serializeMove("Test Status", game.player1.deck.popleft(),
                           game.player2.deck.popleft(), True, True)
        self.assertEqual(len(game.moves), 1)
        move = game.moves[0]
        self.assertEqual(move["Status"], "Test Status")
        self.assertEqual(move["p1NumCards"], 0)
        self.assertEqual(move["p2NumCards"], 0)
        oneCard = move["p1Card"]
        self.assertEqual(oneCard["isFaceUp"], "True")
        self.assertEqual(oneCard["Suit"], p1TestCard.suit)
        self.assertEqual(oneCard["Value"], p1TestCard.value)
        twoCard = move["p2Card"]
        self.assertEqual(twoCard["isFaceUp"], "True")
        self.assertEqual(twoCard["Suit"], p2TestCard.suit)
        self.assertEqual(twoCard["Value"], p2TestCard.value)
    
    def test_tied_ran_out(self):
        game = Game()
        game.player1.deck = deque()
        game.player2.deck = deque()
        game.player1.deck.append(Card(DIAMONDS, 6))
        game.player2.deck.append(Card(CLOVERS, 6))
        game.player1.deck.append(Card(DIAMONDS, 7))
        game.player2.deck.append(Card(CLOVERS, 7))
        game.player1.deck.append(Card(DIAMONDS, 8))
        game.player2.deck.append(Card(CLOVERS, 8))
        game.player2.deck.append(Card(CLOVERS, 9))
        game.player2.deck.append(Card(CLOVERS, 8))
        game.play(False)
        self.assertEqual(game.moves[0]["Status"], "Starting Game")
        self.assertEqual(game.moves[1]["Status"], "Tie, time for war!")
        self.assertEqual(game.moves[2]["Status"], "Tie, time for war!")
        self.assertEqual(game.moves[3]["Status"], "Tie again, time for war!")
        self.assertEqual(game.moves[4]["Status"], "Tie, time for war!")
        self.assertEqual(game.moves[5]["Status"], "Tie again, time for war!")
        self.assertEqual(game.moves[6]["Status"], "Tied and ran out of cards! Reshuffling")

    def test_no_tie(self):
        game = Game()
        game.player1.deck = deque()
        game.player2.deck = deque()
        game.player1.deck.append(Card(DIAMONDS, ACE))
        game.player1.deck.append(Card(HEARTS, QUEEN))
        game.player1.deck.append(Card(HEARTS, ACE))
        game.player1.deck.append(Card(SPADES, 7))
        game.player1.deck.append(Card(HEARTS, JACK))

        game.player2.deck.append(Card(SPADES, 5))
        game.player2.deck.append(Card(SPADES, KING))
        game.player2.deck.append(Card(DIAMONDS, 7))
        game.player2.deck.append(Card(DIAMONDS, 6))
        game.player2.deck.append(Card(SPADES, QUEEN))
        game.play(False)
        self.assertEqual(game.moves[0]["Status"], "Starting Game")
        self.assertEqual(game.moves[1]["Status"], "Player 1 victory")
        self.assertEqual(game.moves[2]["Status"], "Player 2 victory")
        self.assertEqual(game.moves[3]["Status"], "Player 1 victory")
        self.assertEqual(game.moves[4]["Status"], "Player 1 victory")
        self.assertEqual(game.moves[5]["Status"], "Player 2 victory")
        self.assertEqual(game.moves[6]["Status"], "Player 1 victory")
        self.assertEqual(game.moves[7]["Status"], "Player 2 victory")
        self.assertEqual(game.moves[8]["Status"], "Player 1 victory")
        self.assertEqual(game.moves[9]["Status"], "Player 2 victory")
        self.assertEqual(game.moves[10]["Status"], "Player 1 victory")
    
    def test_tie(self):
        game = Game()
        game.player1.deck = deque()
        game.player2.deck = deque()
        game.player1.deck.append(Card(DIAMONDS, JACK))
        game.player1.deck.append(Card(HEARTS, 7))
        game.player1.deck.append(Card(HEARTS, ACE))
        game.player1.deck.append(Card(SPADES, QUEEN))
        game.player1.deck.append(Card(HEARTS, ACE))

        game.player2.deck.append(Card(SPADES, JACK))
        game.player2.deck.append(Card(SPADES, 6))
        game.player2.deck.append(Card(DIAMONDS, 2))
        game.player2.deck.append(Card(DIAMONDS, KING))
        game.player2.deck.append(Card(SPADES, 5))
        game.play(False)
        self.assertEqual(game.moves[0]["Status"], "Starting Game")
        self.assertEqual(game.moves[1]["Status"], "Tie, time for war!")
        self.assertEqual(game.moves[1]["p1Card"]["Value"], game.moves[1]["p2Card"]["Value"])
        self.assertEqual(game.moves[2]["Status"], "Tie, time for war!")
        self.assertEqual(game.moves[3]["Status"], "Player 1 victory")
        self.assertEqual(game.moves[4]["Status"], "Player 2 victory")
    
    def test_tie_again(self):
        game = Game()
        game.player1.deck = deque()
        game.player2.deck = deque()
        game.player1.deck.append(Card(DIAMONDS, JACK))
        game.player1.deck.append(Card(HEARTS, 7))
        game.player1.deck.append(Card(HEARTS, ACE))
        game.player1.deck.append(Card(SPADES, QUEEN))
        game.player1.deck.append(Card(HEARTS, ACE))
        
        game.player2.deck.append(Card(SPADES, JACK))
        game.player2.deck.append(Card(SPADES, 6))
        game.player2.deck.append(Card(DIAMONDS, ACE))
        game.player2.deck.append(Card(DIAMONDS, KING))
        game.player2.deck.append(Card(SPADES, 5))
        game.play(False)
        self.assertEqual(game.moves[0]["Status"], "Starting Game")
        self.assertEqual(game.moves[1]["Status"], "Tie, time for war!")
        self.assertEqual(game.moves[1]["p1Card"]["Value"], game.moves[1]["p2Card"]["Value"])
        self.assertEqual(game.moves[2]["Status"], "Tie, time for war!")
        self.assertEqual(game.moves[3]["Status"], "Tie again, time for war!")
        self.assertEqual(game.moves[3]["p1Card"]["Value"], game.moves[3]["p2Card"]["Value"])
        self.assertEqual(game.moves[4]["Status"], "Tie, time for war!")
        self.assertEqual(game.moves[5]["Status"], "Player 1 victory")



        
            
