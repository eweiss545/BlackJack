##
## ai_clairvoyant5.py
##

from ai_perfect4 import *

class AIPlayerClairvoyant(AIPlayerPerfectNoMemory):
    """
    Implements a player with limited foresight.  Specifically, at the beginning of a
    round, the player can see the next two cards that will be dealt from the shoe, i.e.,
    the dealer face_down and face_up cards.  The player adjusts it's bet to be either
    min_bet or self.other_bet*self.min_bet (for other_bet>=1) and other_bet*self.bankroll
    (for other_bet < 1) (when possible).

    Notebook Task: Fine a good value for other_bet.  Explain why and how you selected
    other_bet.  Use equity curves and statistics as appropriate.

    Extra Credit:  Design a version of AIPlayerClairvoyant called AIPlayerSeer that looks at
    all possible outcomes for the current round, and then bets and acts accordingly. Can you
    see how to extend your solution to n possible future rounds? Add an AIPlayerSeer section
    to your notebook if you do this task.
    """


    def __init__(self, bankroll, min_bet, shoe, other_bet):
        '''This function initializes the Clairvoyant strategy'''
        super().__init__(bankroll, min_bet)
        self.deck=shoe
        self.other_bet=other_bet


    def bet(self):
        """
        Returns how much money to bet for the current hand. We summed the total probabilities
        and found when the probability of busting was greater than the probability of
        finishing with a hand of 17 or more. The AIPlayerClairvoyant will only bet a higher
        amount if the dealer's hand is greater than 13 but less than 17.
        """
        cheat=self.deck.cards[self.deck.next_card:self.deck.next_card+2]
        hand_dealer=BlackjackHand(cheat)
        dealer_tot=hand_dealer.get_value()
        if hand_dealer.soft_value()==False: #If the hand is hard
            if 13<=dealer_tot<=17:
                if self.other_bet>=1:
                    return self.other_bet*self.min_bet
                else:
                    if self.other_bet*self.bankroll<self.min_bet:
                        return self.min_bet
                    else:
                        return self.other_bet*self.bankroll
            else:
                return self.min_bet
        else: #If the hand is soft
            return self.min_bet


def AIPlayerClairvoyanttest():
    '''This function tests the AIPlayerClairvoyant'''
    bankroll = 20
    min_bet = 10
    other_bet=4
    hand=[Card('K','S'),Card('6','S')]
    s = Shoe(1, infinite=False,cards=hand)
    p = AIPlayerClairvoyant(bankroll, min_bet,s,other_bet)
    assert p.bet()==min_bet*other_bet
    hand2=[Card('4','S'),Card('6','S')]
    s2 = Shoe(1, infinite=False,cards=hand2)
    p2 = AIPlayerClairvoyant(bankroll, min_bet,s2,other_bet)
    assert p2.bet()==min_bet
    hand3=[Card('A','S'),Card('A','S')]
    s3 = Shoe(1, infinite=False,cards=hand3)
    p3 = AIPlayerClairvoyant(bankroll, min_bet,s3,other_bet)
    assert p3.bet()==min_bet
    hand4=[Card('Q','S'),Card('K','S')]
    s4 = Shoe(1, infinite=False,cards=hand4)
    p4 = AIPlayerClairvoyant(bankroll, min_bet,s4,other_bet)
    assert p4.bet()==min_bet
    hand5=[Card('A','S'),Card('2','S')]
    s5 = Shoe(1, infinite=False,cards=hand5)
    p5 = AIPlayerClairvoyant(bankroll, min_bet,s5,other_bet)
    assert p5.bet()==min_bet
    hand6=[Card('A','S'),Card('8','S')]
    s6 = Shoe(1, infinite=False,cards=hand6)
    p6 = AIPlayerClairvoyant(bankroll, min_bet,s6,other_bet)
    assert p6.bet()==min_bet

    #Testing for when other_bet is less than 1
    other_bet=0.5
    hand7=[Card('K','S'),Card('4','S')]
    s7 = Shoe(1, infinite=False,cards=hand7)
    p7 = AIPlayerClairvoyant(bankroll, min_bet,s7,other_bet)
    assert p7.bet()==other_bet*bankroll
    hand8=[Card('A','S'),Card('2','S')]
    s8 = Shoe(1, infinite=False,cards=hand8)
    p8 = AIPlayerClairvoyant(bankroll, min_bet,s8,other_bet)
    assert p8.bet()==min_bet


AIPlayerClairvoyanttest()
