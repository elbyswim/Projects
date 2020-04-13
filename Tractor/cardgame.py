import random

class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

    def show(self):
        print('{} of {}'.format(self.value, self.suit))


class Deck:
    def __init__(self, n=1):
        values = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        suits = ['Spades', 'Diamonds', 'Clubs', 'Hearts']
        self.cards = []
        for i in range(n):
            for suit in suits:
                for value in values:
                    self.cards.append(Card(value, suit))

    def show(self):
        for card in self.cards:
            card.show()

    def shuffle(self):
        for n in range(5):
            for i in range(len(self.cards)):
                j = random.randint(i - 1, len(self.cards) - 1)
                self.cards[i], self.cards[j] = self.cards[j], self.cards[i]

    def draw(self):
        return self.cards.pop()


class Player:
    def __init__(self, name):
        self.name = name
        self.cards = []

    def draw(self, deck):
        self.cards.append(deck.draw())

    def show_hand(self):
        for card in self.cards:
            card.show()
