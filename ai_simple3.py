##
## ai_simple3.py
##

from simulate import *

class AIPlayerBadLuck(Player):
    """
    AIPlayer that assumes dealer's hole card is a 10, hits
    until their own hand value is above 10 + dealer up card.
    Always uses minimum bet.
    """
    def __init__(self, bankroll, min_bet):
        """
        Constructor for AIPlayer.
        """
        super().__init__(bankroll, min_bet)



    def next_move(self):
        """
        Returns 'h' for hit and 's' for stand
        """
        # Get the value of the AIPlayer's hand:
        pv = self.tot()
        dv = self.hand_dealer.get_value()
        while pv < min(10 + dv + 1, 21):
            return 'h'

    def bet(self):
        """
        Returns how much money to bet for the current hand.
        """
        return self.min_bet

class AIPlayerMimicDealer(Player):
    """
    AIPlayer that hits until their hand is 17 or above.

    Notebook Task: In your notebook compare the performance between AIMimicDealer
    and AIPlayerBadLuck.  Is there a clear winner? Support your result by looking
    at each strategies Expected Gains (EG), EG Confidence Intervals. Use a mean
    comparison test(s).  Provide example equity curves.
    """
    def __init__(self, bankroll, min_bet):
        """
        Constructor for AIPlayerMimicDealer.
        """
        super().__init__(bankroll, min_bet)

    def next_move(self):
        """
        Returns 'h' for hit and 's' for stand
        """
        pv = self.tot()
        if pv < 17:
            # Hit if hand value is less than 17
            return 'h'
        else:
            # Otherwise, stand
            return 's'

    def bet(self):
        """
        Returns how much money to bet for the current hand.
        """
        return self.min_bet


class AIPlayerS17(Player):
    """
    AIPlayer that hits until their hand is 17 or higher, but also hits
    on a soft 17.  Bets twice the minimum per round (if possible).

    Notebook Task: Perform the same analysis between AIPlayerS17 and AIPlayerMimicDealer
    as you did between AIMimicDealer and AIPlayerBadLuck.  Is one of the strategies clearly
    better than the other?
    """
    def __init__(self, bankroll, min_bet):
        """
        Constructor for AIPlayerS17.
        """
        super().__init__(bankroll, min_bet)



    def next_move(self):
        """
        Returns 'h' for hit and 's' for stand
        """
        pv = self.tot()
        if pv < 17:
            # hit if hand value is less than 17
            return 'h'
        elif pv == 17 and  self.hand_player.soft_value()== True:
            # Hit if hand value is 17 and ace is soft
            return 'h'
        else:
            # Otherwise, stand
            return 's'

    def bet(self):
        """
        Returns how much money to bet for the current hand.
        """
        if self.bankroll >= 2*self.min_bet:
            return 2*self.min_bet
        else:
            return self.min_bet


def AIPlayerMimicDealer_test():
    '''This function tests the AIPlayerMimicDealer class'''
    num_decks = 2
    bankroll = 10
    min_bet = 1
    d = DealerH17()
    s = Shoe(num_decks, infinite=False)
    p = AIPlayerMimicDealer(bankroll, min_bet)
    p.hand_player=BlackjackHand([Card('A','H'),Card('10','S'),Card('6','C')])
    assert p.next_move()=='s'
    p.hand_player=BlackjackHand([Card('4','H'),Card('5','S'),Card('6','C')])
    assert p.next_move()=='h'
    p.hand_player=BlackjackHand([Card('10','H'),Card('5','S'),Card('5','C')])
    assert p.next_move()=='s'
    p.hand_player=BlackjackHand([Card('10','H'),Card('5','S'),Card('6','C')])
    assert p.next_move()=='s'

AIPlayerMimicDealer_test()


def AIPlayerS17_test():
    '''This function tests the AIPlayerS17'''
    num_decks = 2
    bankroll = 10
    min_bet = 1
    d = DealerH17()
    s = Shoe(num_decks, infinite=False)
    p = AIPlayerS17(bankroll, min_bet)
    #Checking for h or s
    p.hand_player=BlackjackHand([Card('A','H'),Card('3','S'),Card('3','C')])
    assert p.next_move()=='h'
    p.hand_player=BlackjackHand([Card('A','H'),Card('10','S'),Card('6','C')])
    assert p.next_move()=='s'
    p.hand_player=BlackjackHand([Card('4','H'),Card('5','S'),Card('6','C')])
    assert p.next_move()=='h'
    p.hand_player=BlackjackHand([Card('10','H'),Card('5','S'),Card('5','C')])
    assert p.next_move()=='s'
    p.hand_player=BlackjackHand([Card('10','H'),Card('5','S'),Card('6','C')])
    assert p.next_move()=='s'

    #Checking for correct betting
    #Standard bet amount
    assert p.bet()==2
    #If bankroll is less than 2* min_bet
    p.bankroll=1.5
    assert p.bet()==1


AIPlayerS17_test()
#
# if __name__ == '__main__':
#     num_decks = 2
#     bankroll = 10
#     min_bet = 1
#     d = DealerH17()
#     s = Shoe(num_decks, infinite=False)
#     p = AIPlayerS17(bankroll, min_bet)
#     g = Game(d, p, s, 20, .8, print_n=10 )
#     g = Game(DealerH17(), AIPlayerBadLuck(50000, 2), Shoe(8), 10**4, .8, print_n=100)
#
#     g.run() # Run Game
#     g.summary() # Print results
