##
## setup2.py
##

from setup1 import *
import random

class BlackjackHand(Hand):
    """
    Represents a Hand of cards in a game of Blackjack.
    """
    def __init__(self, cards=None):
        """
        Setups up a Blackjack hands containing a list of cards.
        """
        if cards == None:
            cards= []
        super().__init__(cards)
        self.soft=None


    def get_value(self):
        """
        Returns the total value of the cards in a BlackjackHand,
        accounting for Aces.
        """

        is_ace=super().has_any('A')
        if super().get_value()+10<=21 and is_ace==True:
            new_score=super().get_value()+10
            self.soft=True
            return new_score
        else:
            self.soft=False
            return super().get_value()


    def soft_value(self):
        """Returns true if best value of hand relies on an Ace being an 11"""
        return self.soft


class Shoe:
    """
    Represents a card shoe containing decks of playing cards.
    """
    def __init__(self, num_decks, infinite=False, cards = []):
        """
        Creates a card shoe containing num_decks of standard playing cards.
        When infinite is False dealing is done by sampling without replacement.
        When infinite is True dealing done by sampling with replacement.
        """
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

        if len(cards) == 0:
            self.cards=deck*num_decks
        else:
            self.cards=cards*num_decks

        self.num_decks = num_decks
        self.infinite = infinite
        self.next_card = 0

        self.shuffle()

    def shuffle(self):
        """
        Randomizes the order of the cards in the shoe when not using
        an infinite deck. Resets .next_card to front of the shoe.
        """
        if self.infinite == False:
            random.shuffle(self.cards)
        self.next_card=0


    def num_dealt(self):
        """
        Returns the number of cards dealt from shoe.
        """
        return self.next_card

    def num_remaining(self):
        """
        Returns the number of un-dealt cards in the shoe.
        """
        return len(self.cards) - self.next_card

    def deal(self, n):
        """Deals n cards.  Returns them as a list."""
        if not self.infinite:
            to_deal = self.cards[self.next_card:self.next_card+n]
            self.next_card = self.next_card + n
            return to_deal
        else:
            self.next_card = self.next_card + n
            return [random.choice(self.cards) for _ in range(n)]


def Shoe_test():
    '''This function tests the shoe class'''
    s1=Shoe(2,False)
    assert len(s1.cards)==104 #Testing for num decks

    c=[Card('2','C'),Card('2','H'),Card('2','D'),Card('2','S')] #Defining cards
    random.seed(100)
    s4=Shoe(1,infinite=False,cards=c)
    assert str(s4.cards[1])=='2D' #Ensuring that the cards are shuffled

    s4.shuffle()
    assert str(s4.cards[1])=='2H' #Shuffle test




Shoe_test()

def BlackjackHand_test():
    '''This function tests the Blackjack Hand function'''
    c1 = Card("7","H")
    c2 = Card("A","D")
    c3 = Card("2","D")
    c4 = Card('10',"C")
    c5 = Card("A","S")
    h2=BlackjackHand([c1,c2,c3])
    assert h2.get_value()==20
    assert h2.soft_value()==True
    h2.add_card(c4)
    assert h2.get_value()==20
    assert h2.soft_value()==False
    h2.add_card(c5)
    assert h2.get_value()==21
    assert h2.soft_value()==False

    h3=BlackjackHand([c2,c5,c1])
    assert h3.get_value()==19
    assert h3.soft_value()==True

BlackjackHand_test()
