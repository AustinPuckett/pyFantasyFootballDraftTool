# pyFantasyFootballDraftTool
A GUI application for fantasy football drafting and analysis. 

## The NBA Metric[^1]

This app imports NFL player's seasonal fantasy points projections (FPTS) and average draft positions (ADPs) to calculate the "points over next best available player" (PONBA or NBA). PONBA (NBA) for a draft pick is calculated by subtracting the FPTS of the user's next pick's best available player from the FPTS of the selected player. See below:

### Example: 
*Current Pick Number = 6 (first round pick)*

*Next Pick Number = 19 (second round pick)*

#### Available Players:
Name - Position - FPTS

+ *Tyreek Hill - WR - 248*
+ *Saquon Barkley RB - 236*
+ *CeeDee Lamb - WR - 222*

#### Best Players Available at the 19th pick (i.e., ADP >= 19):
+ *Garrett Wilson - WR - 200*
+ *Najee Harris - RB - 203*

#### Available Player's NBA calculations:
+ *Tyreek Hill - WR: NBA = (248 - 200) = 48*
+ *Saquon Barkley - RB: NBA = (236 - 203) = 33*
+ *CeeDee Lamb - WR: NBA = (222 - 200) = 22*


Since Tyreek Hill has the highest NBA, he is the best selection with the current draft pick.

[^1]: It's hypothesized that this algorithm works best for picks 3 through 10, since picks 1, 2, 11, and 12 occur at what's called "the turn", where draft picks for a fantasy team occur subsequently. The NBA metric likely fails for these picks at the turn.


## How to Use this Tool

To use this tool for 2023, run the main.py file. On the start-up screen, click the import adp button and select "FantasyPros_2023_Overall_ADP_Rankings.csv". Then click the import projections button and select "FantasyPros_Fantasy_Football_Projections_ALL.csv". Then click the import draft order button and select "Sample Draft Order.csv". Then click the begin draft button.

To select a player to draft, double click on the player in the player list, then press the submit pick button. To view drafted players, click the draft board button.

### Current bugs: 

- [ ] Users have the ability to submit a blank pick when the only a single click is used on the player list: make sure to double click the player in the list (their info should populate in the "Draft Player" section of the UI.

### Future improvements:

- [ ] Add "previous pick" functionality, allowing the user to go back and edit a prior draft pick.
- [ ] Use a UI window to add draft order, team, and keeper information.
- [ ] Make the draft tool work for various roster structures and league sizes.
