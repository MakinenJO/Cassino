from PyQt5.Qt import pyqtSignal, QObject

class Card(QObject):
    select_signal = pyqtSignal([int, str])
    
    def __init__(self, value, suit):
        super(Card, self).__init__()
        self.value = value
        self.suit = suit
        self.selected = False
        
    def select(self):
        self.selected = True
        self.select_signal.emit(self.value, self.suit)
        
    def deselect(self):
        self.selected = False
        
    def get_hand_value(self):
        if self.value == 1:
            return 14
        
        if self.suit == 'Spades' and self.value == 2:
            return 15
        
        if self.suit == 'Diamonds' and self.value == 10:
            return 16
        
        return self.value
        
    def __str__(self):
        return '{} of {}'.format(self.value, self.suit)