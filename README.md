# pyFantasyFootballDraftTool
A GUI application for fantasy football drafting and analysis. 

This app imports NFL player's seasonal fantasy points projections (FPTS) and average draft positions (ADPs) to calculate the "points over next best available player" (PONBA or NBA). PONBA (NBA) for a draft pick is calculated by subtracting the FPTS of the user's next pick's best available player from the FPTS of the selected player. See below:

Example: 
Current Pick Number = 6 (first round pick)
Next Pick Number = 19 (second round pick)

Available Players:
Name - Position - FPTS
Tyreek Hill - WR - 248
Saquon Barkley RB - 236
CeeDee Lamb - WR - 222

Best Players Available at the 19th pick (i.e., ADP >= 19):
Garrett Wilson - WR - 200
Najee Harris - RB - 203

Available Player's NBA calculations:
Tyreek Hill - WR: NBA = (248 - 200) = 48
Saquon Barkley - RB: NBA = (236 - 203) = 33
CeeDee Lamb - WR: NBA = (222 - 200) = 22

Since Tyreek Hill has the highest NBA, he is the best selection with the current draft pick.

*Note: It's hypothesized that this algorithm works best for picks 3 through 10, since picks 1, 2, 11, and 12 occur at what's called "the turn", where draft picks for a fantasy team occur subsequently. The NBA metric likely fails for these picks at the turn.
