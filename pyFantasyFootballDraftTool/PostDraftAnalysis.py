import sqlite3 as sql
from matplotlib import pyplot as plt
import pandas as pd

# def generate_draft_report(db_conn):
#     cursor = db_conn.cursor()
#
#     query = '''SELECT * FROM players p
#                 WHERE draft_indicator = 1
#                 JOIN draft_board db on p.'''
#     cursor.execute(query)
    
def export_results(df, file_path):
    # file_path = r''
    df.to_csv(file_path)

def analyze_draft(input_file_path, output_filepath):
    '''Determine the roster position for each drafted player.

    #TODO: Make roster structure a variable input. It is currently set to a 1 QB, 2 RB, 2 WR, 1 TE, 1 DST, and 2 FLEX structure.'''
    df = pd.read_csv(input_file_path)
    df['POS Roster Rank'] = 0
    df['Roster POS'] = ''
    df['Roster Spot'] = ''

    fantasy_teams = list(df['fantasy_team'].unique())
    postions = list(df['POS'].unique())
    # postions = ['WR']

    for team in fantasy_teams:
        for pos in postions:
            df.loc[(df['fantasy_team'] == team) & (df['POS'] == pos), 'POS Roster Rank'] = df[(df['fantasy_team'] == team) & (df['POS'] == pos)]['FPTS'].rank(method='first', ascending=False)

            df.loc[(df['fantasy_team'] == team) & (df['POS'].isin(['RB', 'WR'])) & (df['POS Roster Rank'] <= 2), 'Roster POS'] = df['POS']
            df.loc[(df['fantasy_team'] == team) & (df['POS'].isin(['QB', 'TE', 'DST'])) & (df['POS Roster Rank'] <= 1), 'Roster POS'] = df['POS']

            df.loc[(df['fantasy_team'] == team) & (df['POS'].isin(['RB', 'WR'])) & (df['POS Roster Rank'] > 2), 'Roster POS'] = 'FLEX'
            df.loc[(df['fantasy_team'] == team) & (df['POS'].isin(['TE'])) & (df['POS Roster Rank'] > 1), 'Roster POS'] = 'FLEX'

    for team in fantasy_teams:
        df.loc[(df['fantasy_team'] == team) & (df['Roster POS'] == 'FLEX'), 'POS Roster Rank'] = df[(df['fantasy_team'] == team) & (df['Roster POS'] == 'FLEX')]['FPTS'].rank(method='first', ascending=False)

    df['Roster Spot'] = df['Roster POS'] + df['POS Roster Rank'].astype(str)

    df.to_csv(output_filepath)