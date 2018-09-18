##
## setup1.py
##
from functools import reduce

class Card:
    """
    Represents a card from a "standard" deck of playing cards that consists
    of 52 Cards in each of the 4 suits of Spades, Hearts, Diamonds, and Clubs.
    Each suit contains 13 cards named:
      Ace, 2, 3, 4, 5, 6, 7, 8, 9, 10, Jack, Queen, King.
    """

    NAME_CONVERSIONS = {
        "1":"1",
        "2":"2",
        "3":"3",
        "4":"4",
        "5":"5",
        "6":"6",
        "7":"7",
        "8":"8",
        "9":"9",
        "10": "10",
        "j":"J",
        "jack":"J",
        "q":"Q",
        "queen":"Q",
        "k":"K",
        "king":"K",
        "ace": "A",
        "a":"A"
        }

    SUIT_CONVERSIONS = {
        "c":"C",
        "club": "C",
        "clubs":"C",
        "s":"S",
        "spades": "S",
        "spade":"S",
        "h":"H",
        "heart":"H",
        "hearts": "H",
        "d":"D",
        "diamond":"D",
        "diamonds": "D"
        }

    def __init__(self, name, suit):
        """
        Stores face card names by their capitalized first letter, e.g.
        'Ace', 'ACE', 'acE', 'a', are all stored as 'A'.
        Numeric card names are stored as their corresponding string, e.g.,
        '1' is stored as '1', '10' is stored as '10'.
        Suit names are handled in a similar manner.

        The final card name is stored in self.name,
        The final card Suit is stored in self.suit.
        """

        name=name.lower()
        norm_name=self.NAME_CONVERSIONS[name]


        suit=suit.lower()
        norm_suit=self.SUIT_CONVERSIONS[suit]

        # Save to internal representation:
        self.name = norm_name
        self.suit = norm_suit


    def __repr__(self):
        """
        Returns a simple human-readable string representing a Card.
        """
        return self.name + self.suit


    def get_value(self):
        """
        Returns the value of a card as an integer.
        """
        if self.name in ['1','2','3','4','5','6','7','8', '9', '10']:
            return int(self.name)
        if self.name in ['J','Q','K']:
            return 10
        if self.name == 'A':
            return 1


class Hand:
    """
    Represents a Hand of cards
    """

    def __init__(self, cards = []):
        """
        Constructor for Hand objects. Optionally takes a card or list of cards.
        """
        self.cards=cards


    def __repr__(self):
        """
        Returns a human-readable string representing a Hand.
        """
        returnValue = ""
        for element in self.cards:
            returnValue += str(element) + ', '
        return returnValue[:-2]

    def add_card(self, card):
        """
        Adds the given card(s) to the Hand.  Accepts a single card or a list of cards.
        """
        #Determines if there are more than one.
        if isinstance(card,list):
            for element in range(len(card)):
                #Creates a new hand
                new_hand=Hand([card[element]])
                #Adds hand to list
                self.cards+= new_hand.cards
        else:
            new_hand=Hand([card])
            self.cards+= new_hand.cards


    def num_cards(self):
        """
        Returns the number of cards in the Hand.
        """
        length=len(self.cards)
        return length

    def get_value(self):
        """
        Returns the total value of the cards in the Hand (where Aces, by
        default, count for 1).
        """
        #Finds all of the values in the cards
        score_list=[Card.get_value(card) for card in self.cards]
        #Sums the scores
        if self.num_cards() > 0:
            total_score=reduce((lambda x,y: x+y),score_list)
            return total_score
        else:
            return 0

    def has_any(self, name):
        """
        Returns True if the Hand contains a card of the given name; otherwise,
        returns False.
        """
        counter = 0
        for element in self.cards:
            if name in str(element):
                counter += 1

        if counter > 0:
            return True
        else:
            return False


def Card_test():
    '''This function tests the card class'''
    c1=Card('quEen','CLub')
    assert c1.name=='Q'
    assert c1.suit=='C'
    c2=Card('jAck','spaDe')
    assert c2.name=='J'
    assert c2.suit=='S'
    c3=Card('3','clubs')
    assert c3.name=='3'
    assert c3.suit=='C'
    c4=Card('A','hearts')
    assert c4.name=='A'
    assert c4.suit=='H'
    c5=Card('aCe','spaDes')
    assert c5.name=='A'
    assert c5.suit=='S'
    c6=Card('KiNg','cLubs')
    assert c6.name=='K'
    assert c6.suit=='C'

Card_test()

def test_get_value():
    '''This function tests the get value function for the card class'''
    c1 = Card('queen','club')
    c2 = Card('aCe','spADes')
    c3 = Card('2', 'H')
    assert c1.get_value() == 10, 'face card case failed'
    assert c2.get_value() == 1, 'ace case failed'
    assert c3.get_value() == 2, 'number card case failed'


test_get_value()

def Hand_add_card_test():
    '''This function tests the add card function in the hand class'''
    c1 = Card("7","H")
    c2 = Card("A","D")
    c3 = Card("2","D")
    h = Hand()
    h.add_card(c1)
    h.add_card([c2, c3])
    h.add_card(c2)
    assert len(h.cards) == 4
    h.add_card(c1)
    assert len(h.cards) == 5
    h.add_card(c1)
    assert len(h.cards) == 6


Hand_add_card_test()

def test_num_card():
    '''This function tests the num card function'''
    c1 = Card("7","H")
    c2 = Card("A","D")
    c3 = Card("2","D")
    h = Hand([])
    h.add_card(c1)
    h.add_card([c2, c3])
    h.add_card(c2)
    h1 = Hand([])
    assert h.num_cards() == 4
    h.add_card(c1)
    assert h.num_cards() == 5
    assert h1.num_cards() == 0

test_num_card()

def test_get_value_hand():
    '''This function tests the get_value for the hand class'''
    c1 = Card("7","H")
    c2 = Card("A","D")
    c3 = Card("2","D")
    c4 = Card('Q', 'D')
    h = Hand([c1,c2,c3])
    h1 = Hand([])
    assert h.get_value() == 10
    h.add_card(c4)
    assert h.get_value() == 20
    h.add_card(c1)
    assert h.get_value() == 27
    assert h1.get_value() == 0

test_get_value_hand()


def test_has_any():
    '''This function tests the has any method'''
    c1 = Card("7","H")
    c2 = Card("A","D")
    c3 = Card("2","D")
    c4 = Card("K","S")
    h = Hand([c1,c2,c3])
    assert h.has_any('7') == True
    assert h.has_any('A') == True
    assert h.has_any('Q') == False
    assert h.has_any('D') == True
    assert h.has_any('C') == False
    h.add_card(c4)
    assert h.has_any('K') == True


test_has_any()
