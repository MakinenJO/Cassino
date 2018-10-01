from deck import Deck
from player import Player, AIPlayer
from validator import is_valid_combo, get_move
from PyQt5.Qt import QObject, pyqtSignal, QSoundEffect, QUrl

class Game(QObject):
    #Modes
    DEAL_ONE = 0
    DEAL_FOUR = 1
    
    logSignal = pyqtSignal(str)
    sweepSignal = pyqtSignal()
    
    def __init__(self, pointlimit,  deal_mode = 0):
        super(Game, self).__init__()
        self.pointlimit = pointlimit
        self.deal_mode = deal_mode
        self.players = []
        self.deck = Deck()
        self.table = []
        self.round = 0
        self.current_player = None
        self.last_pick = None
        self.cardDraw = 1   #multiplier to account for draw with cards
        self.spadeDraw = 1  #multiplier to account for draw with spades
        self.one_human = False #True if only one human player in game
        self.setup_sound()
        
        
    def setup_sound(self):
        self.deal_sound = QSoundEffect()
        self.deal_sound.setSource(QUrl.fromLocalFile('sound/playcard.wav'))
        
        if self.deal_mode == Game.DEAL_FOUR:
            self.deal_sound.setLoopCount(4)
        
        
    def add_player(self, name, difficulty):
        if difficulty == 5:
            self.players.append(Player(name))
        else:
            self.players.append(AIPlayer(name, difficulty))
            
        self.one_human = self.is_only_one_human()
        
        
    def new_round(self):
        self.deck = Deck()
        self.deck.populate()
        self.deck.shuffle()
        self.table = []
        for player in self.players:
            player.deck = []
            player.sweeps = 0
        self.round += 1
        self.current_player = self.players[0]
        
        
    def next_player(self):
        self.current_player = self.players[(self.players.index(self.current_player)+1)%len(self.players)]
             
                    
    def do_action(self):
        player = self.current_player
        hand_card = None
        for card in player.hand:
            if card.selected:
                hand_card = card
                
        if hand_card == None:
            return False
                
        table_cards = [card for card in self.table if card.selected]
                    
        if len(table_cards) == 0:
            player.hand.remove(hand_card)
            self.table.append(hand_card)
            self.logSignal.emit('{} trailed with {}\n'.format(player, hand_card))
                    
        else:
            if type(player) is Player:
                if not is_valid_combo(hand_card.get_hand_value(), [c.value for c in table_cards]):
                    self.logSignal.emit('Invalid move\n')
                    return False
                       
            for c in table_cards:
                player.deck.append(c)
                self.table.remove(c)
            player.hand.remove(hand_card)
            player.deck.append(hand_card)
            self.last_pick = player
                
            self.logSignal.emit('{} used {} to capture:\n{}\n'.format(player, hand_card, '\n'.join([str(c) for c in table_cards])))
            
            if len(self.table) == 0:
                player.sweeps += 1
                self.logSignal.emit('Sweep!\n')
                self.sweepSignal.emit()
            
        return True 
    
    
    def select_move_for_ai(self):
        player = self.current_player
        hand_c, table_c = get_move(player.hand, self.table, player.difficulty)
        
        hand_c.select()
        
        if table_c != None:
            for c in table_c:
                c.select()
            
            
    def initial_deal(self):
        #Deals four cards to each player and the table, two cards at a time
        self.logSignal.emit('\nDealing new round....\n\n')
        for i in range(2):
            for player in self.players:
                player.hand.append(self.deck.draw_top_card())
                player.hand.append(self.deck.draw_top_card())
            self.table.append(self.deck.draw_top_card())
            self.table.append(self.deck.draw_top_card())
    
    
    def deal(self):
        if self.deal_mode == Game.DEAL_ONE:
            self.deal_one()
            
        if self.deal_mode == Game.DEAL_FOUR:
            self.deal_four()
    
    def deal_one(self):
        if self.deck.get_size() > 0:
            self.current_player.hand.append(self.deck.draw_top_card())
            self.deal_sound.play()
            if self.deck.get_size() == 0:
                self.logSignal.emit('\n\nLast deal!\n')
                
            
    def deal_four(self): #Deal four cards to each player, two cards at a time
        if sum([len(p.hand) for p in self.players]) == 0 and self.deck.get_size() > 0:
            self.logSignal.emit('\n\nDealing new cards...\n')
            self.deal_sound.play()
            
            for i in range(2):
                for player in self.players:
                    player.hand.append(self.deck.draw_top_card())
                    player.hand.append(self.deck.draw_top_card())
                    
            if self.deck.get_size() == 0:
                self.logSignal.emit('Last deal!\n')
                
            
            
    def end_round(self):
        player = self.last_pick
        table_cards = [card for card in self.table]
        
        self.logSignal.emit('\n\n{} was the last to capture and received:\n{}\n'.format(player, '\n'.join([str(c) for c in self.table])))
        self.logSignal.emit('\nEnd of round\n')
        
        for c in table_cards:
            player.deck.append(c)
            self.table.remove(c)
            
        self.count_points()
        
        if max([p.score for p in self.players]) >= self.pointlimit:
            self.logSignal.emit('\n\nGame over, score limit reached\n')
            self.logSignal.emit('Final scores:\n--------------\n')
            for p in reversed(sorted(self.players, key=lambda p: p.score)):
                self.logSignal.emit('{}: {}\n'.format(p.name, p.score))
            return True #Return True if game ended
        
        self.players.append(self.players.pop(0)) #rotate players
        return False
        
            
    def count_points(self):
        points = []
        
        for i in range(len(self.players)):
            p = 0
            player = self.players[i]
            for card in player.deck:
                if card.value == 10 and card.suit == 'Diamonds':
                    p += 2
                if card.value == 2 and card.suit == 'Spades':
                    p += 1
                if card.value == 1:
                    p += 1
                    
            points.append(p + player.sweeps)
            
        cards = [len(p.deck) for p in self.players]
        spades = [len([c for c in p.deck if c.suit == 'Spades']) for p in self.players]
        
        #Count the winner for most cards and spades
        #If there is a draw, the corresponding multiplier is incremented and points will be carried to next round
        
        if cards.count(max(cards)) == 1:
            points[cards.index(max(cards))] += 1 * self.cardDraw
            self.cardDraw = 1    
        else:
            self.cardDraw += 1
            
        if spades.count(max(spades)) == 1:
            points[spades.index(max(spades))] += 2 * self.spadeDraw
            self.spadeDraw = 1
        else:
            self.spadeDraw += 1
            
        
        
        for i in range(len(self.players)):
            self.players[i].score += points[i]
            self.logSignal.emit('{} received {} points.\n'.format(self.players[i].name, points[i]))
        
    
    def is_only_one_human(self): #Determine if only one human player in game
        count = 0
        for p in self.players:
            if type(p) is Player:
                count += 1
                
        if count == 1:
            return True
        
        return False
    