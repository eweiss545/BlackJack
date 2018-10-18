CS40 BlackJack - Python

This project, completed for Brown U.'s Intro to Scientific Computing & Problem Solving, creates a game of BlackJack, several AI Black Jack Players, and finally contains an analysis of each strategy using Jupyter Notebook. 

Interactive play: In order to play rounds of BlackJack (you vs dealer), you need only run simulate.py after downloading all files. 

AI strategies: Most of the files create AI Players that will play according to a specific strategy. The higher the number in the file name, (generally) the more complex the strategy. You can find a detailed description of each strategy in the comments. 

Ai_simple 3 contains 3 strategies, all relatively simple: AIPlayerBadLuck, AIPlayerMimicDealer, and AIPlayer S17. These are not very effective strategies. 

Ai_perfect4 contains AIPlayerPerfectNoMemory, which implements the optimal strategy for an infinite deck. To look at how this player runs, please view ai_perfect4.ipynb, which shows a simulation of this strategy against a dealer across 1 million rounds and 1 thousand rounds (to show that an Expected Gain, given a low number of rounds, will be considerably off from the "true" Expected Gain). It also includes an analysis at the end. 

The rest follows suit. Ai_clairvoyant5.py, ai_hilo6.py, and ai_better7.py all contain other AI strategies. The file ai_clairvoyant.ipynb runs that same player, AIClairvoyant, in three games against the dealer with three different betting strategies. Each game was played in 10,000 rounds. The intention of ai_clairvoyant.ipynb was to find the best possible betting method for this player. 

Those are all the included files. To find a more detailed description of the project, you can view the pdf Project 3 - Blackjack included in the repository.
