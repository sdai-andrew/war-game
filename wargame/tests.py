import unittest
from django.test import TestCase
from wargame.models import Player
from game import *

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
            self.assertIn(card.color, COLORS)
        deckSet = set(deck)
        self.assertEqual(len(deck), len(deckSet))
    
    def test_game_creation(self):
        game = Game()
        self.assertEqual(game.moves, [])
        self.assertEqual(len(game.player1.deck), 32)
        self.assertEqual(len(game.player2.deck), 32)
        for card in game.player1.deck:
            self.assertNotIn(card, game.player2.deck)
        for card in game.player2.deck:
            self.assertNotIn(card, game.player1.deck)
    
    def test_serialize_move(self):
        game = Game()
        p1TestCard = Card(SPADES, RED, JACK)
        p2TestCard = Card(DIAMONDS, BLACK, 3)
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
        self.assertEqual(oneCard["Color"], p1TestCard.color)
        self.assertEqual(oneCard["Value"], p1TestCard.value)
        twoCard = move["p2Card"]
        self.assertEqual(twoCard["isFaceUp"], "True")
        self.assertEqual(twoCard["Suit"], p2TestCard.suit)
        self.assertEqual(twoCard["Color"], p2TestCard.color)
        self.assertEqual(twoCard["Value"], p2TestCard.value)

        
            
