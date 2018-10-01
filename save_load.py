from game import Game
from card import Card

def save(path, game, logtxt, move_count):
    suitnames = {'Spades': 'S', 'Clubs': 'C', 'Diamonds': 'D', 'Hearts': 'H'}
    file = open(path, 'w')
    
    
    pointlimit = str(game.pointlimit)
    deal_mode = str(game.deal_mode)
    file.write(pointlimit + ',' + deal_mode + '\n')
    
    deckstr = ''
    for c in game.deck.cards:
        deckstr += str(c.value)+suitnames[c.suit] + ','
    if deckstr != '':
        file.write(deckstr[:-1] + '\n')
    else:
        file.write('0\n')
    
    tablestr = ''
    for c in game.table:
        tablestr += str(c.value)+suitnames[c.suit] + ','
    if tablestr != '':
        file.write(tablestr[:-1] + '\n')
    else:
        file.write('0\n')
    
    file.write(str(len(game.players)) + '\n')
    
    for p in game.players:
        pstring = str(p.difficulty) + ',' + p.name + ',' \
                    + str(p.score) + ',' + str(p.sweeps) + ','
        
        handstr = ''
        for c in p.hand:
            handstr += str(c.value)+suitnames[c.suit] + ';'
        if handstr != '':
            pstring += handstr[:-1] + ','
        else:
            pstring += '0,'
        
        
        cardstr = ''
        for c in p.deck:
            cardstr += str(c.value)+suitnames[c.suit] + ';'
        if cardstr != '':
            pstring += cardstr[:-1]
        else:
            pstring += '0'
        
        file.write(pstring + '\n')
        
    currentplr = str(game.players.index(game.current_player))
    if game.last_pick != None:
        lastpick = str(game.players.index(game.last_pick))
    else:
        lastpick = '-1'
    cardraw = str(game.cardDraw)
    spadraw = str(game.spadeDraw)
    movecount = str(move_count)
    
    file.write(currentplr + ',' + lastpick + ',' + cardraw + ','\
               + spadraw + ',' + movecount + '\n')
    
    
    file.write(logtxt + '\n')
    
    file.close()
 
 
    
def load(file_path):
    suitnames = {'S': 'Spades', 'C': 'Clubs', 'D': 'Diamonds', 'H': 'Hearts'}
    file = open(file_path, 'r')
    
    line = file.readline().rstrip()
    line = line.split(',')
    pointlimit, deal_mode = int(line[0]), int(line[1])
    
    game = Game(pointlimit, deal_mode)
    
    deckstr = file.readline().rstrip()
    cards = deckstr.split(',')
    
    if cards[0] != '0':
        for c in cards:
            value = int(c[:-1])
            suit = suitnames[c[-1]]
            card = Card(value, suit)
            game.deck.cards.append(card)
        
    tablestr = file.readline().rstrip()
    cards = tablestr.split(',')
    
    if cards[0] != '0':
        for c in cards:
            value = int(c[:-1])
            suit = suitnames[c[-1]]
            card = Card(value, suit)
            game.table.append(card)
        
    plrnum = int(file.readline().rstrip())
    
    for i in range(plrnum):
        plrstr = file.readline().rstrip()
        info = plrstr.split(',')
        difficulty, name, score, sweeps = int(info[0]), info[1],\
                                            int(info[2]), int(info[3])
        hand = info[4].split(';')
        deck = info[5].split(';')
        
        game.add_player(name, difficulty)
        game.players[i].score = score
        game.players[i].sweeps = sweeps
        
        if hand[0] != '0':
            for c in hand:
                value = int(c[:-1])
                suit = suitnames[c[-1]]
                card = Card(value, suit)
                game.players[i].hand.append(card)
                
        if deck[0] != '0':
            for c in deck:
                value = int(c[:-1])
                suit = suitnames[c[-1]]
                card = Card(value, suit)
                game.players[i].deck.append(card)
                
    info = file.readline().rstrip()
    info = info.split(',')
    curr, last, cardraw, spadraw, movecount = int(info[0]), int(info[1]), \
                        int(info[2]), int(info[3]), int(info[4])
    
    game.current_player = game.players[curr]
    game.last_pick = game.players[last]
    game.cardDraw = cardraw
    game.spadeDraw = spadraw
    
    logmsg = file.read()
    
    
    file.close()
    return game, logmsg, movecount
    
    