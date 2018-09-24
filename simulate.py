##
## simulate.py
##

from setup2 import *
import numpy as np
import statsmodels.stats.api as sms
import sys

BJP = 1.95

def play_round(d, p, s, print_cards):
    """Plays a round of CS4 Blackjack using Dealer d, Player p and Shoe s

    Returns (bet_amount, gain, round_result)

    ---
    Progression of round of play is as follows:

    0) Each round of play is signalled by a call to p.new_round() and d.new_round().

    1) The p.bet() method is called to determine a player's initial bet amount.

    2) As player and dealer cards are dealt the appropriate .add(player, dealer) method is used to add these cards to an
    internal representation (.hand_player, .hand_dealer) of the information *currently*
    available to the player and dealer.

    The p.next() method is called at each player decision point in the game to determine
    their next action.

    3) After the player stands (p.next()=='s'), the dealer object d.next() method is then used
    to determine the dealer's final hand.

    Game play stops as soon as a winner is determined. i.e., after the initial deal (on a player
    and or dealer blackjack), while the player is hitting (if the player goes bust), after the
    player stands and while the the dealer is hitting (if dealer goes bust), or based on final
    player and dealer .tot() hand values.

    Player gains are determined by how they were won or lost, winning with a natural blackjack
    (An Ace and 10 present in the first two cards, no natural dealer black jack) is paid according
    to house Blackjack payoff amount BJP (1.5 in standard Blackjack, 1.95 for CS4 Blackjack),
    otherwise all over payoffs are 1:1.
    """
    d.new_round(); p.new_round()

    bet = p.bet()
    if bet < p.min_bet or bet > p.bankroll: raise Exception('Bad bet amount!')

    [face_down, face_up] = s.deal(2)
    d.add(dealer=[face_down, face_up])
    p.add(player=s.deal(2), dealer=[face_up])

    if print_cards: print(p)

    if d.tot() == 21 or p.tot() == 21:
        p.add(dealer=[face_down])
        if print_cards: print(p)
        if p.tot() == d.tot(): return (bet, 0, 'PD_BJ') # Player BJ and Dealer BJ
        if d.tot() == 21: return (bet, -1, 'D_BJ') # Dealer BJ
        return (bet, BJP, 'P_BJ')  # Player Blackjack!

    while p.tot() < 21 and p.next_move() == 'h':
        p.add(player=s.deal(1))
        if print_cards: print(p)

    p.add(dealer=[face_down]) # Assumes player gets to see the hole card even if they bust

    if p.tot() > 21:
        return (bet, -1, 'P_Bust') # Player Busted

    if print_cards: print(p)
    while d.next_move() == 'h' and d.tot() < 21:
        c = s.deal(1)
        d.add(dealer=c)
        p.add(dealer=c)
        if print_cards: print(p)

    if d.tot() > 21: return (bet, 1, 'D_Bust')  # Dealer Busted
    if d.tot() == p.tot(): return (bet, 0, 'PD_Draw')  # Draw
    if d.tot() < p.tot(): return (bet, 1, 'P_Won')  # Player Won
    return (bet, -1, 'P_Lost')  # Player Lost

class Game:
    """
    Simulates a Blackjack game session. During a game, initiated via .run(), many rounds are played.
    At the end of every round the player's .bankroll (capital) adjusted appropriately.
    When shoe changes (i.e., shuffles) occur they are indicated to the player via the Player.new_shoe() method.
    """

    def __init__(self, dealer, player, shoe, max_rounds, penetration=.8, print_n = 0):
        """
        Sets up Game with dealer, layer, shoe and shoe instances. max_rounds of play
        is total rounds of play per .run(), assuming player does not go broke, penetration
        is the fraction of shoe cards dealt before re-shuffling the shoe.

        Setting print_n = k will print play for the first round, and then every k rounds.
        """
        self.player = player
        self.dealer = dealer
        self.shoe = shoe
        self.max_rounds = max_rounds
        self.shuffle_after = penetration*shoe.num_decks*52
        self.print_n = print_n
        self.results = []

    def run(self):
        """
        Runs a game of Blackjack, results are stored in g.results are as follows:
        ('round', 'bet', 'gain', 'type', 'shuffle', 'EG', 'final_bankroll')
        """
        self.results = np.zeros(self.max_rounds, \
                           dtype= [('round', 'i4'), ('bet', 'f8'), ('gain', 'f8'), \
                                   ('type','U7'), ('shuffle', '?'), ('EG', 'f8'), ('final_bankroll', 'f8'), \
                                   ])
        rounds_played = 0; avg = 0;
        balance = self.player.bankroll
        self.player.new_shoe()
        while rounds_played < self.max_rounds and balance >= self.player.min_bet:
            print_stats = (self.print_n>0) and (self.print_n and rounds_played % self.print_n == 0)
            r = play_round(self.dealer, self.player, self.shoe, print_stats)
            rounds_played += 1

            shuffle = False
            if self.shoe.num_dealt() > self.shuffle_after:
                self.shoe.shuffle()
                self.player.new_shoe()
                shuffle = True

            avg = avg+r[1]
            balance = balance + r[0]*r[1]
            self.player.bankroll = balance
            r = (rounds_played,) + r + (shuffle, avg/rounds_played, balance)
            if print_stats: print(r)
            self.results[rounds_played-1] = r

        self.rounds_played = rounds_played

    def summary(self):
        """
        Prints of a summary of the action, based on a Game.results.
        """
        w=0;l=0;t=0; tb=0; tw=0; avg=0
        for r in self.results:
            w += r[3] in ['P_BJ','P_Won', 'D_Bust']
            l += r[3] in ['D_BJ', 'P_Bust', 'P_Lost']
            t += r[3] in ['PD_Draw', 'PD_BJ']
            tb += r[1]
            tw += r[1]*(1+r[2])
            avg += r[2]

        print(f"Total Rounds {w+l+t} [Wins: {w} Losses: {l} Ties: {t}]")
        print(f"tot_bet = {tb} tot_won = {tw} (won-bet)={tw-tb}")
        print(f"E(won-bet) = {(tw-tb)/self.rounds_played} (won-bet)/tb = {(tw-tb)/tb} EG = {avg/self.rounds_played}");
        print(f"EG 95% CI = {sms.DescrStatsW(self.results['gain']).tconfint_mean()}")
        print(f"edge = {tw/tb}") #Printing the edge


class Player():
    """
    Blackjack player class.  Used during Game play, to determine player decisions during each round of play.

    * This version creates an Interactive Blackjack player which prompts the user to hit or stand. *

    ----
    See documentation for the Game class and the play_round function to understand the progression of
    play and how each method in this class is used.
    ----
    """

    def __init__(self, bankroll=100, min_bet=2):
        """bankroll is the amount of initial capital.
           min_bet is minimum amount allowed to bet on each round."""
        self.hand_player = BlackjackHand()  # internal representation for player cards
        self.hand_dealer = BlackjackHand()  # internal representation for dealer cards
        self.bankroll = bankroll
        self.min_bet = min_bet
        self.truecount=0 #Initializing the counting strategy for HiLo

    def new_round(self):
        """
        Called at the beginning of each round of play.
        """
        self.hand_player.cards = []  # Setup for new hands
        self.hand_dealer.cards = []

    def new_shoe(self):
        """
        Called at the beginning of every game and whenever the shoe is shuffled.
        """
        # Hint: When new_shoe is called it is time to order a drink (casino option) or stretch (healthy option)
        # AND for card counters to reset their card counts.
        self.truecount=0



    def bet(self):
        """Returns player bet amount."""
        print(f'bet: amount = {self.min_bet}')  # New players should start with the minimum
        return self.min_bet

    def add(self, player=[], dealer=[]):
        """Used to add player and dealer cards to .hand_player and .hand_player as they become available
        to the player. """
        # Adds list of player cards to player_hand
        # Adds list of dealer cards to dealer_hand
        self.hand_player.add_card(player)
        self.hand_dealer.add_card(dealer)

    def tot(self):
        """Returns the value of the player's current hand"""
        # Easy access to get value of player hand
        return self.hand_player.get_value()

    def __repr__(self):
        """
        Prints out the Player's hand as ASCII cards and the hand's value.
        """
        return f'[Dealer: {self.hand_dealer}]({self.hand_dealer.get_value()})' + \
               f'[Player: {self.hand_player}]({self.hand_player.get_value()})'

    def next_move(self):
        """
        Returns the players next move.  In CS4 Blackjack this is hit ('h') or stand ('s'). Real blackjack
        also supports buying insurance ('i') doubling ('d') and splitting ('S').
        """
        # Get input from the USER
        inp = ""
        while len(inp) < 1:
            # Request input
            inp = input("Would you like to hit, stand or quit? (h/s/q) ")

            # Error Check!
            if len(inp) < 1:
                continue

            # Evaluate input
            else:
                if inp[0].lower() == "h":
                    return 'h'
                elif inp[0].lower() == "s":
                    return 's'
                elif inp[0].lower() == "q":
                    sys.exit()
                else:
                    print("Invalid input\n")
                    inp = ""


class DealerH17(Player):
    """
    Represents a Dealer in a game of Blackjack.

    This version creates a "Hard 17" version that hits until her total is 17 or more.
    Note: The "Soft 17" version requires the dealer to also hit on a soft 17.
    """

    def __init__(self):
        """
        Constructor for Dealer.
        """
        Player.__init__(self)

    def add(self, dealer=[], player=[]):
        """Used to add player and dealer cards to .hand_player and .hand_player as they become available
        to the player. """
        # Adds list of player cards to player_hand
        # Adds list of dealer cards to dealer_hand
        self.hand_player.add_card(player)
        self.hand_dealer.add_card(dealer)

    def tot(self):
        """Returns the value of the dealer's current hand"""
        # Easy access to get value of player hand
        return self.hand_dealer.get_value()

    def next_move(self):
        """
        Determines whether or not to draw another card. Returns True if the
        Dealer should; otherwise, returns False.
        """
        if self.hand_dealer.get_value() < 17:
            # Hit if hand value is less than 17
            return 'h'
        else:
            # Otherwise, stand
            return 's'

if __name__ == '__main__':
    num_decks = 2
    bankroll = 20
    min_bet = 10
    s = Shoe(num_decks, infinite=False)
    p = Player(bankroll, min_bet)
    d = DealerH17()
    g = Game(d, p, s, 10, .8, print_n=1)

    print('Welcome to Interactive Blackjack')
    print('Fixed bet size = ', p.min_bet)
    print('BJ round results are reported as follow:')
    print("('round #', 'player bet amount', 'player gain factor', 'type of outcome', \n" +
          " 'deck shuffled', 'Expected Gain', 'ending bankroll')")
    g.run() # Run Game
    g.summary() # Print results
