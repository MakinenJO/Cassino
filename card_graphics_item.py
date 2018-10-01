from PyQt5.QtMultimedia import QSoundEffect
from PyQt5.Qt import QGraphicsPixmapItem, QPixmap, QUrl

class CardGraphicsItem(QGraphicsPixmapItem):
    suitnames = {'Spades': 'S', 'Clubs': 'C', 'Diamonds': 'D', 'Hearts': 'H'}
    
    def __init__(self, card):
        super(CardGraphicsItem, self).__init__()
        self.path = 'img/' + str(card.value) + CardGraphicsItem.suitnames[card.suit]
        self.show_face()
        self.setScale(0.12)
        self.card = card
        self.click_sound = QSoundEffect()
        self.click_sound.setSource(QUrl.fromLocalFile('sound/playcard.wav'))
        
    
    def mousePressEvent(self, *args, **kwargs):
        self.click_sound.play()
        
        if not self.card.selected:
            self.select()
             
        else:
            self.deselect()
            
        
    def select(self):
        self.moveBy(0, -20)
        self.card.select()
        
    def deselect(self):
        self.moveBy(0, 20)
        self.card.deselect()
        
    def show_face(self):
        self.setPixmap(QPixmap(self.path))
        
    def show_back(self):
        self.setPixmap(QPixmap('img/red_back')) #img/red_back
        
        
    def __str__(self):
        return '{} of {}'.format(self.card.value, self.card.suit)