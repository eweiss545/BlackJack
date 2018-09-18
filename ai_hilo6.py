##
## ai_hilo6.py
##


from ai_clairvoyant5 import *

class AIPlayerHiLo(AIPlayerPerfectNoMemory):
    """Implements a High-Low card Counting AI.  Uses the "True Count" to adjust bet size.

    Notebook Task: Find a good value for bet_by_count.  Explain why and how you arrived
    at the values you selected.  Use equity curves and statistics as appropriate. Explain
    what happens when bet_by_count is too aggressive. Include some statistics or equity
    curves.
    """
    def __init__(self,bankroll,min_bet,num_deck,bet_by_count):
        '''Initializing the HiLo player'''
        super().__init__(bankroll,min_bet)
        self.bet_by_count=bet_by_count
        self.num_deck = num_deck
        self.played_cards=[]


    def add(self, player=[], dealer=[]):
        """Used to add player and dealer cards to .hand_player and .hand_player as they become available
        to the player. """
        # player = added player cards, # dealer = added dealer cards
        self.hand_player.add_card(player)
        self.hand_dealer.add_card(dealer)
        #creates another variable to hold cards as they are added
        self.played_cards = player + dealer
        # count the number of cards played
        self.counter+= len(self.played_cards)


        for card in self.played_cards:
            card_val = card.get_value()
            if card_val in [2,3,4,5,6]:
                self.runcount += 1
            elif card_val in [10,1]:
                self.runcount -= 1
            else:
                self.runcount+= 0


    def bet(self):
        '''This function is called to determine the right bet amount'''

        #Dividing the runcount by the number of decks left to get truecount.
        decks_left = self.num_deck - (self.counter / 52)
        if decks_left!=0:
            self.truecount=self.runcount / decks_left
            self.truecount=round(self.truecount)

        #Implementing the counting to the betting scheme.
        if self.truecount<=0:
            return self.min_bet
        elif self.truecount>=len(self.bet_by_count):
            obet=self.bet_by_count[-1]
            if obet>=1:
                return obet*self.min_bet
            else:
                bet=obet*self.bankroll
                if bet>self.min_bet:
                    return bet
                else:
                    return self.min_bet
        else:
            obet=self.bet_by_count[self.truecount]
            if obet>=1:
                return obet*self.min_bet
            else:
                bet=obet*self.bankroll
                if bet>self.min_bet:
                    return bet
                else:
                    return self.min_bet


def ai_hilo_test():
    bbc1=[1,1.4,1.5,0.5]
    bankroll=20
    min_bet=2
    deck=[Card('2','H'),Card('2','D'),Card('2','S'),Card('2','C'),\
    Card('3','H'),Card('3','D'),Card('3','S'),Card('3','C'),\
    Card('4','H'),Card('4','D'),Card('4','S'),Card('4','C'),\
    Card('5','H'),Card('5','D'),Card('5','S'),Card('5','C'),\
    Card('6','H'),Card('6','D'),Card('6','S'),Card('6','C'),\
    Card('7','H'),Card('7','D'),Card('7','S'),Card('7','C'),\
    Card('8','H'),Card('8','D'),Card('8','S'),Card('8','C'),\
    Card('9','H'),Card('9','D'),Card('9','S'),Card('9','C'),\
    Card('10','H'),Card('10','D'),Card('10','S'),Card('10','C'),\
    Card('J','H'),Card('J','D'),Card('J','S'),Card('J','C'),\
    Card('Q','H'),Card('Q','D'),Card('Q','S'),Card('Q','C'),\
    Card('K','H'),Card('K','D'),Card('K','S'),Card('K','C'),\
    Card('A','H'),Card('A','D'),Card('A','S'),Card('A','C')]
    c2 = Card('2','C')
    c3 = Card('7','H')
    c4 = Card('A','S')
    c5 = Card('4','C')
    c6 = Card('3', 'S')
    c7 = Card('A','S')
    c8 = Card('Q','C')
    c9 = Card('K', 'S')
    s1=Shoe(1,infinite=False,cards=deck)
    p1=AIPlayerHiLo(bankroll,min_bet,1,bbc1)
    p1.add(player=[c2,c3], dealer=[c4])
    assert p1.bet()==2
    assert p1.runcount==0
    assert p1.truecount==0
    p1.add(player=[c5,c6], dealer=[c3])
    assert p1.bet()==2*1.5
    assert p1.runcount==2
    assert p1.truecount==2
    ## Testing when count > len(bet_by_count)
    p1.add(player=[c5,c6,c5,c6], dealer=[c5])
    assert p1.bet()==bankroll * 0.5
    assert p1.runcount==7
    assert p1.truecount==9
    ## Testing when count is negative
    p1.add(player=[c7,c7,c8,c8,c9,c9], dealer=[c7,c7])
    assert p1.bet()==2
    assert p1.runcount== -1
    assert p1.truecount==-2

# Testing with multiple decks
    s2=Shoe(1,infinite=False,cards=deck*5)
    p2=AIPlayerHiLo(bankroll,min_bet,5,bbc1)
    p2.add(player=[c2,c3], dealer=[c4])
    assert p2.bet()==2
    assert p2.runcount==0
    assert p2.truecount==0
    p2.add(player=[c5,c6,c6,c6], dealer=[c3])
    assert p2.bet()==2*1.4
    assert p2.runcount==4
    assert p2.truecount==1
    p2.add(player=[c5,c6,c6,c6], dealer=[c3])
    assert p2.bet()==2*1.5
    assert p2.runcount==8
    assert p2.truecount==2



ai_hilo_test()
