##
### ## ai_better7.py
##


from ai_hilo6 import *

class AIPlayerBetter(AIPlayerHiLo):
    """Implements a High-Low card Counting AI.  Uses the "True Count" to adjust
    bet size as well as hit/stand strategy
    """
    def __init__(self,bankroll,min_bet,num_deck,bet_by_count):
        '''Initializing the AIPlayerBetter'''
        super().__init__(bankroll,min_bet,num_deck,bet_by_count)



    def next_move(self):
        """
        Returns 'h' for hit and 's' for stand
        """
        #Tuecount needs to be updated every next move because it's placed within
        #bet method in HiLo
        decks_left = self.num_deck - (self.counter / 52)
        if decks_left!=0:
            self.truecount=self.runcount / decks_left
            self.truecount=round(self.truecount)

        dv = self.hand_dealer.get_value()
        pv = self.tot()

        if pv==12 and dv == 2:
            indx = 3
        elif pv==12 and dv == 3:
            indx=2
        elif pv==12 and dv == 4:
            indx=0
        elif pv==12 and dv == 5:
            indx=-1
        elif pv==13 and dv == 2:
            indx=-1
        elif pv==14 and (dv == 1 or dv == 11):
            indx=9
        elif pv==15 and dv == 7:
            indx=10
        elif pv==15 and dv == 8:
            indx=10
        elif pv==15 and dv == 9:
            indx=8
        elif pv==15 and dv == 10:
            indx=4
        elif pv==15 and (dv == 1 or dv == 11):
            indx=9
        elif pv==16 and dv == 7:
            indx=9
        elif pv==16 and dv == 8:
            indx=7
        elif pv==16 and dv == 9:
            indx=5
        elif pv==16 and dv == 10:
            indx=0
        elif pv==16 and (dv == 1 or dv == 11):
            indx=8
        else:
            indx = 100

        if indx <100: # indx has been updated
            if self.truecount >= indx:
                self.standcount+= 1
                return 's'
            else:
                self.hitcount+=1
                return 'h'
        else:
            if self.hand_player.soft_value()== False: #if player hard
                if dv in [1,2,3,4,5,6,7,8,9,10] and pv in [4,5,6,7,8,9,10,11]:
                    self.hitcount+= 1
                    return 'h'
                elif dv in [2,3] and pv == 12:
                    self.hitcount+= 1
                    return 'h'
                elif dv in [1,7,8,9,10] and pv in [12,13,14,15,16]:
                    self.hitcount+=1
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

def ai_better_test():
     bet_count=[1,1.4,1.5,0.5]
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
     c10 = Card('5','C')
     s1=Shoe(1,infinite=False,cards=deck)
     p1=AIPlayerBetter(bankroll,min_bet,1,bet_count)
     p1.add(player=[c2,c3], dealer=[c4])
     #p1 total = hard 9, #d total = 11 runcount = 0
     assert p1.bet()==2
     assert p1.runcount==0
     assert p1.truecount==0
     assert p1.next_move() == 's'
     assert p1.standcount == 1
     p1.add(player=[c5], dealer=[c3])
     #p1 total = hard 13, dealer = 18 runcount = 1
     assert p1.bet()==2*1.4
     assert p1.runcount==1
     assert p1.truecount==1
     assert p1.next_move()=='s'
     assert p1.standcount == 2
     p1.add(player=[c6])
#     #p1 total = hard 16, dearl = 18 runcount = 3
     assert p1.bet()==2*1.5
     assert p1.runcount==2
     assert p1.truecount==2
     assert p1.next_move()=='s'
     assert p1.standcount == 3
     p2=AIPlayerBetter(bankroll,min_bet,4,bet_count)

     ## Testing indx cases - stand
     p2.add(player=[c2,c8], dealer=[c5])
     #p1 total = hard 12, #d total = 4 runcount = 1
     assert p2.bet()==2
     assert p2.runcount==1
     assert p2.truecount==0
     assert p2.next_move()=='s'
     assert p2.standcount == 1
     assert p2.hitcount == 0


     ## Testing indx cases - hit
     p2.add(player=[c5], dealer=[c10])
     #p1 total = hard 16, #d total = 9 runcount = 3
     assert p2.bet()==2*1.4
     assert p2.runcount==3
     assert p2.truecount==1
     assert p2.next_move()=='h'
     assert p2.standcount == 1
     assert p2.hitcount == 1


ai_better_test()
