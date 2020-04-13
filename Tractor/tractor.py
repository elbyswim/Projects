from cardgame import Card
from cardgame import Deck
from cardgame import Player

class Game:
    def __init__(self, players, decks=2):
        self.decks = decks
        self.cards = Deck(self.decks)
        self.team1 = [players[0], players[2]]
        self.team2 = [players[1], players[3]]
        self.defending_team = None
        self.trump_level = None
        self.trump_suit = None
        self.attacking_points = 0
        self.start_player = None

