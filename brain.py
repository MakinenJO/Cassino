brain_multipliers = { 1: {'10D_favour'  :   -2,     #how much special cards are favoured
                          '2S_favour'   :   -1,
                          'ace_favour'  :   -1,
                          'card_favour' :   +0,     #how much card/spade amount or sweep is favoured
                          'spade_favour':   +0, 
                          'sweep_favour':   -1,
                          'tactic_next' :   +0,     #try placing card tactically for good pickup next round, yes=1 no=0
                          'max_len'     :   +2},    #max amount of table cards to pick
                          
                      2: {'10D_favour'  :   +0,
                          '2S_favour'   :   +0,
                          'ace_favour'  :   +1,
                          'card_favour' :   +1,
                          'spade_favour':   +1,
                          'sweep_favour':   +3,
                          'tactic_next' :   +0,
                          'max_len'     :   +3},
                      
                      3: {'10D_favour'  :   +2,
                          '2S_favour'   :   +4,
                          'ace_favour'  :   +5,
                          'card_favour' :   +1,
                          'spade_favour':   +3,
                          'sweep_favour':   +0,
                          'tactic_next' :   +1,
                          'max_len'     :   +5},
                      
                      4: {'10D_favour'  :   +10,
                          '2S_favour'   :   +5,
                          'ace_favour'  :   +5,
                          'card_favour' :   +1,
                          'spade_favour':   +2,
                          'sweep_favour':   +5,
                          'tactic_next' :   +1,
                          'max_len'     :   +20}}