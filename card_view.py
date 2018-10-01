'''
A QGraphicsView widget that shows cards
'''
from PyQt5.Qt import QGraphicsView, QGraphicsScene
from card_graphics_item import CardGraphicsItem


class CardView(QGraphicsView):
    
    def __init__(self, parent=None):
        super(CardView, self).__init__(parent)
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.setMinimumWidth(400)
        self.cards = []
        
        
    def show_cards(self):
        for card in self.cards:
            card.show_face()
            
    def hide_cards(self):
        for card in self.cards:
            card.show_back()
            
    def deselect_all(self):
        for card in self.cards:
            if card.card.selected:
                card.deselect()
                
    def auto_select(self): #for AI card selection
        for card in self.cards:
            if card.card.selected:
                card.show_face()
                card.select()   
            
        
    def add_card(self, card):        
        new_card = CardGraphicsItem(card)    
        self.cards.append(new_card)
        mv = 90*(len(self.cards)-1)
        new_card.moveBy(mv,0)
        self.scene.addItem(new_card)
        self.scene.update()
        
        if len(self.cards) > 10:
            for card in self.cards:
                card.setScale(0.1)
        
        self.reset_bounds()
    
            
    def del_cards(self, cards_to_keep):
        for c in self.cards:
            if c.card not in cards_to_keep:
                self.remove_card_from_scene(c)
                c.card.deselect()
                
        self.cards[:] = [c for c in self.cards if c.card in cards_to_keep]

        self.reset_bounds()

        
    def remove_card_from_scene(self, card):
        self.scene.removeItem(card)
        
        for other in self.cards[self.cards.index(card):]:
            other.moveBy(-90,0)
           
        self.reset_bounds()
        
        
    def update_scene(self, current_cards):
        self.del_cards(current_cards)
                
        for c in current_cards:
                if c not in [ca.card for ca in self.cards]:
                    self.add_card(c)
        
            
    def reset_bounds(self): #ensures cards are neatly displayed in view
        bounds = self.scene.itemsBoundingRect()
        self.scene.setSceneRect(bounds)



class HandCardView(CardView): #A card_view subclass that only allows a single card to be chosen at a time
    def __init__(self, parent = None):
        super(HandCardView, self).__init__(parent)
        
    def add_card(self, card):
        CardView.add_card(self, card)
        card.select_signal.connect(self.hand_card_select)
        
    def remove_card_from_scene(self, card):
        card.card.select_signal.disconnect()
        CardView.remove_card_from_scene(self, card)
        
    
    def hand_card_select(self, value, suit): #ensures only one hand card is selected at a time
        
        for c in self.cards:
            if c.card.selected and (c.card.value != value or c.card.suit != suit):
                c.deselect()
        
    