class Player:
    
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.sweeps = 0
        self.hand = []
        self.deck = []
        self.difficulty = 5
        
    def print_hand(self):
        print('{}\'s hand:'.format(self.name))
        for card in self.hand:
            print('{}: {}'.format(self.hand.index(card)+1, card))
        print()
        
    
    def __str__(self):
        return self.name

        
        
class AIPlayer(Player):
    #Difficulties
    braindead = 0
    easy = 1
    normal = 2
    hard = 3
    expert = 4
    
    def __init__(self, name, difficulty):
        super(AIPlayer, self).__init__(name)
        self.difficulty = difficulty
    