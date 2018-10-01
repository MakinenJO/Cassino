# -*- encoding: utf-8 -*-

import itertools
from itertools import chain
import brain
#from card import Card

def is_valid_combo(hand, table):
    #return boolean stating if attempted move is legal
    #ie. if table values can be arranged to subsets that each equal hand value
    #may overflow memory if over 12 cards chosen
        
    
    #check for some obvious illegal situations
    if len(table) < 1 or sum(table) % hand != 0:
        return False
    
    for value in table:
        if value > hand:
            return False
    
    #reduce size of table by removing values equal to hand    
    table = [val for val in table if val != hand]
    if len(table) == 0:
        return True
    
    #sort so comparison possible later
    table.sort()
    
    #get list of all possible combinations in table that add up to hand value
    combos = []
    
    for i in range(1, len(table)+1):
        combinations = list(itertools.combinations(table, i))
        for combination in combinations:
            if sum(combination) == hand:
                combos.append(combination)
    
    #iterate through all combinations of generated combinations
    for i in range(1, len(combos)+1):
        subcombos = list(itertools.combinations(combos, i)) # generate a list of subcombinations from combos
        
        for y in subcombos: #go through each subcombo
            merged = list(chain.from_iterable(y)) #merge subcombo to list in order to compare with table
            if sorted(merged) == table: # if a subcombo matches with table, the move is legal
                return True
            
    
    return False



def get_move(hand_cards, table_cards, difficulty):
    if difficulty == 0:
        return hand_cards[0], None
    
    mul = brain.brain_multipliers[difficulty]
    
    hand_choice, table_choice, points = determine_best_move(hand_cards, table_cards, mul)
                        
    if (hand_choice == None or points < 3) and len(hand_cards) > 1 and mul['tactic_next']==1:
    #if nothing can be picked up or move has low points, determine best card to place on table
        max_pts = 0
        for card in hand_cards:
            #find best move next turn if 'card' is placed on table this turn
            points = determine_best_move([c for c in hand_cards if c != card], list(chain.from_iterable([[card], table_cards])), mul)[2]

            #substract points if card is valuable
            #raise these numbers to make AI more careful
            if card.get_hand_value() > 13:
                points -= 8
            if card.suit == 'Spades':
                points -= 5
                
            if points > max_pts:
                max_pts = points
                if table_choice == None or points > 5: 
                    hand_choice = card
                    table_choice = None
                
    if hand_choice == None: #if still no moves found, place card with smallest value on table, avoiding spades
        hand_choice = min(hand_cards, key=lambda c: c.get_hand_value()+mul['spade_favour'] if c.suit=='Spades' else c.get_hand_value())
    

    return hand_choice, table_choice
        
                        
def determine_best_move(hand_cards, table_cards, mul):
    max_points = 0
    table_size = len(table_cards)
    hand_choice = None
    table_choice = None
    
    for i in range(1, min(table_size+1, mul['max_len'])):
        combinations = list(itertools.combinations(table_cards, i)) #form combinations from table cards
        
        for combination in combinations:
            for card in hand_cards:                                 #try all hand and table combinations
                
                if is_valid_combo(card.get_hand_value(), [c.value for c in combination]):               #test if move legal
                    points = count_move_pts(card, combination, table_size, mul) #determine goodness of move
                    
                    if points > max_points: #keep current move if it has the highest points so far
                        hand_choice = card
                        table_choice = combination
                        max_points = points
                        
    return hand_choice, table_choice, max_points


def count_move_pts(hand_card, table_cards, table_len, mul):
    pts = 0
    pts += len(table_cards) * mul['card_favour'] #add points for amount of cards
    for card in chain.from_iterable([[hand_card], table_cards]): #add points for special cards and spades
        if card.value == 1:
            pts += mul['ace_favour']
        if card.value == 10 and card.suit == 'Diamonds':
            pts += mul['10D_favour']
        if card.value == 2 and card.suit == 'Spades':
            pts += mul['2S_favour']
        if card.suit == 'Spades':
            pts += mul['spade_favour']
            
    if len(table_cards) == table_len: #add points if move is a sweep
        pts += mul['sweep_favour']
        
    return pts
        
        
        
# from card import Card
# from deck import Deck

# c1 = Card(3, 'Spades')
# c2 = Card(2, 'Diamonds') 
# c3 = Card(7, 'Hearts')
# c4 = Card(13, 'Hearts')
# c5 = Card(4, 'Clubs')
# c6 = Card(9, 'Hearts')
# c7 = Card(2, 'Clubs')
# c8 = Card(10, 'Diamonds')
# c9 = Card(5, 'Diamonds')
#  
# hand = [c1,c2,c3,c4]
# table = [c5,c6,c7,c8]

# hand = []
# table = []
# deck = Deck()
# deck.shuffle()
# for i in range(4):
#     hand.append(deck.draw_top_card())
#       
# for i in range(5):
#     table.append(deck.draw_top_card())
#       
# hand_c, table_c = get_move(hand, table)
#  
# print('{}'.format([str(c) for c in hand]))
# print('{}'.format([str(c) for c in table]))
# print('{}'.format(str(hand_c)))
# if table_c:
#     print('{}'.format([str(c) for c in table_c]))
# else:
#     print('None')
'''
TODO:

AI:n toiminnan periaatteet:
muodosta comboja iteroimalla -> testaa onko hyväksytty -> pisteytä -> jos korkeimmat pisteet tähän mennessä, säilytä combo -> kun kaikki käyty läpi,
tee siirto säilytetyllä combolla -> jos ei ole siirtoa, päätä, mikä kortti asetetaan pöytään -> päätös voidaan tehdä esim. valitsemalla arvoltaan pienin,
tai seuraavasti -> laita yksi kortti kerrallan pöydälle ja katso miten hyviä comboja muilla korteilla nyt voisi nostaa -> valitse kortti, jolla paras mahdollinen
nosto ensi vuorolla -> erikoiskorttien asettamisesta pöytään miinuspisteitä 

AI:ssa ::--> kutsu get_move -funktiota -> funktio palauttaa siirron kortteina -> nämä kortit asetetaan valituiksi -> suoritetaan siirto normaalisti

eri vaikeusasteita -- braindead, easy, normal, hard, enigma jne.
'''