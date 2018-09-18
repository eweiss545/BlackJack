##
## ai_perfect4.py
##

from ai_simple3 import *

class AIPlayerPerfectNoMemory(Player):
    """
    Represents a perfect (non-card counting, non-cheating) Player
    in a game of Blackjack. It implements the optimal strategy for an
    infinite deck.

    Notebook Task: Plot example equity curves.  Compare the measured EG
    with the theoretical    EG.  Do the confidence intervals seem
    reasonable?  Use an appropriate statistical test to EG and the
    theoretical EG.
    """
    def __init__(self, bankroll, min_bet):
        """
        Constructor for AIPlayerPerfectNoMemory.
        """
        super().__init__(bankroll, min_bet)


    def next_move(self):
        """
        Returns 'h' for hit and 's' for stand
        """
        dv = self.hand_dealer.get_value()
        pv = self.tot()
        if self.hand_player.soft_value()== False: #if player hard
            if dv in [1,2,3,4,5,6,7,8,9,10] and pv in [4,5,6,7,8,9,10,11]:
                self.hitcount+= 1
                return 'h'
            elif dv in [2,3] and pv == 12:
                self.hitcount+= 1
                return 'h'
            elif dv in [1,7,8,9,10] and pv in [12,13,14,15,16]:
                self.hitcount+= 1
                return 'h'
            else:
                self.standcount+=1
                return 's'
        else: #if player is soft
            if dv in [1,2,3,4,5,6,7,8,9,10] and pv in [12,13,14,15,16,17]:
                self.hitcount+= 1
                return 'h'
            elif dv in [1,9,10] and pv == 18:
                self.hitcount+= 1
                return 'h'
            else:
                self.standcount+=1
                return 's'


    def bet(self):
        """
        Returns how much money to bet for the current hand.
        """
        return self.min_bet

def AIPlayerPerfectNoMemory_test():
    '''This function tests the AIPlayerPerfectNoMemory'''
    num_decks = 2
    bankroll = 10
    min_bet = 1
    d = DealerH17()
    s = Shoe(num_decks, infinite=True)
    p = AIPlayerPerfectNoMemory(bankroll, min_bet)
    #Checking for h or s
    #hard hand testing
    p.hand_player=BlackjackHand([Card('A','H'),Card('10','S'),Card('6','C')])
    p.hand_dealer=BlackjackHand([Card('A','C')])
    assert p.next_move()=='s'
    assert p.standcount == 1
    p.hand_player=BlackjackHand([Card('4','H'),Card('5','S'),Card('6','C')])
    p.hand_dealer=BlackjackHand([Card('9','H')])
    assert p.next_move()=='h'
    assert p.hitcount == 1
    p.hand_player=BlackjackHand([Card('10','H'),Card('5','S'),Card('5','C')])
    p.hand_dealer=BlackjackHand([Card('3','S')])
    assert p.next_move()=='s'
    assert p.standcount == 2
    p.hand_player=BlackjackHand([Card('10','H'),Card('5','S'),Card('6','C')])
    p.hand_dealer=BlackjackHand([Card('3','S')])
    assert p.next_move()=='s'
    assert p.standcount == 3
    #soft hand testing
    p.hand_player=BlackjackHand([Card('A','H'),Card('2','S'),Card('2','C')])
    p.hand_dealer=BlackjackHand([Card('3','S')])
    assert p.next_move()=='h'
    assert p.hitcount == 2
    p.hand_player=BlackjackHand([Card('A','H'),Card('2','S'),Card('7','C')])
    p.hand_dealer=BlackjackHand([Card('9','S')])
    assert p.next_move()=='s'
    assert p.standcount == 4
    #blackjack test
    p.hand_player=BlackjackHand([Card('A','H'),Card('2','S'),Card('8','C')])
    p.hand_dealer=BlackjackHand([Card('9','S')])
    assert p.next_move()=='s'
    assert p.standcount == 5


AIPlayerPerfectNoMemory_test()
