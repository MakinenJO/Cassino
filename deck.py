from card import Card
from random import shuffle

class Deck():
    
    def __init__(self):
        self.cards = []
        
    def populate(self):
        self.cards = self.create_cards()
        
    def create_cards(self):
        cards = []
        for suit in ['Clubs', 'Diamonds', 'Spades', 'Hearts']:
            for val in range(1, 14):
                cards.append(Card(val, suit))
                
        return cards
    
    def shuffle(self):
        shuffle(self.cards)
        
    def draw_top_card(self):
        return self.cards.pop()
    
    def get_size(self):
        return len(self.cards)
        
    def __str__(self):
        ret = ''
        for card in self.cards:
            ret += str(card) + '\n'
            
        return ret
            
        