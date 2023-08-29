import os
import pandas as pd
from datetime import date
import json
import sqlite3 as sql
import PostDraftAnalysis


class ImportDataModel():
    def __init__(self, db_conn):
        self.pick_info = None
        self.draft_df = None
        self.player_df = None
        self.conn = db_conn

        self.drop_tables()

    def create_adp_table(self, upload_file):
        df = pd.read_csv(upload_file)
        df.loc[df['player_pos'] == 'DST', 'player_team'] = ''
        # TODO: Clean and verify data
        df.to_sql(name='adps', con=self.conn)
        self.conn.commit()

    def create_projections_table(self, upload_file):
        df = pd.read_csv(upload_file)
        df.loc[df['player_pos'] == 'DST', 'player_team'] = ''
        # TODO: Clean and verify data
        df.to_sql(name='projected_points', con=self.conn)
        self.conn.commit()

    def create_draft_table(self, upload_file):
        df = pd.read_csv(upload_file)
        df['FPTS'] = None
        df['NBA'] = None
        df['AVG'] = None

        # TODO: Clean and verify data
        df.to_sql(name='draft_board', con=self.conn)
        self.conn.commit()

    def create_draft_tables(self):
        # Append ADP to players table
        query = '''SELECT pp.player_name, pp.player_team, pp.player_pos, pp.FPTS, adps.AVG, adps.rank, db.keeper_indicator
                    FROM projected_points pp
                    JOIN adps ON pp.player_name = adps.player_name AND pp.player_team = adps.player_team
                    LEFT JOIN draft_board db ON pp.player_name = db.player_name AND pp.player_team = db.player_team;
                    '''
        df = pd.read_sql(query, self.conn)
        df['draft_indicator'] = df['keeper_indicator']
        df.loc[df['draft_indicator'].isna(), 'draft_indicator'] = 0
        df = df[df['AVG'].notna()]
        df.to_sql(name='players', con=self.conn)
        self.conn.commit()

    def drop_tables(self):
        pass
        # query = '''DROP TABLE adps'''
        # self.conn.execute(query)
        # query = '''DROP TABLE projected_points'''
        # self.conn.execute(query)
        # query = '''DROP TABLE draft_order'''
        # self.conn.execute(query)
        # query = '''DROP TABLE draft'''
        # self.conn.execute(query)


class DraftRoomModel():
    '''Accesses the draft_board table.

    draft_board table fields:
    pick_number
    round
    pick_subnumber
    team_id
    fantasy_team
    keeper_indicator
    player_name
    player_pos
    player_team
    FPTS
    NBA
    AVG
    '''

    def __init__(self, db_conn):
        self.pick_number = 1
        self.pick_round = 1
        self.pick_subnumber = 1
        self.fantasy_team = None
        self.fantasy_team_id = None
        self.player_name = None
        self.player_pos = None
        self.player_team = None
        self.keeper_indicator = None
        self.fpts = None
        self.nba = None
        self.adp = None

        self.conn = db_conn

    def create(self, entry_dict):
        cursor = self.conn.cursor()
        pick_number, player_name, player_pos, player_team, fpts, nba, avg = [entry_dict['pick_number'],
                                                                                  entry_dict['player_name'],
                                                                                  entry_dict['player_pos'],
                                                                                  entry_dict['player_team'],
                                                                                  entry_dict['FPTS'],
                                                                                  entry_dict['NBA'],
                                                                                  entry_dict['AVG'],
                                                                                  ]
        try:
            # Update player draft status
            cursor.execute(f'''UPDATE players SET draft_indicator = 1
                                WHERE player_name = ?''', (player_name,)) # TODO: Add POS = ? AND Team = ?;
            self.conn.commit()

            # Post player selection to the draft board
            cursor.execute(f'''UPDATE draft_board SET player_name = ?, player_pos = ?, player_team = ?, FPTS = ?, NBA = ?, AVG = ? 
                                WHERE pick_number = ?''', (player_name, player_pos, player_team, fpts, nba, avg, pick_number))

            # cursor.execute(f'''SELECT * FROM players
            #                             WHERE draft_indicator = 1''')
        except:
            #TODO: Error handling
            pass

        cursor.close()

    def create_many(self, entry_list):
        try:
            for entry_dict in entry_list:
                self.create(entry_dict)
        except:
            #TODO: Error handling
            pass

    def get(self, pick_number):

        self.pick_number = pick_number

        cursor = self.conn.cursor()
        cursor.execute(f"PRAGMA table_info(draft_board)")
        columns = [col[1] for col in cursor.fetchall()]

        cursor.execute(f'''SELECT *
                            FROM draft_board db
                            WHERE pick_number = ?
                            ''', (self.pick_number,))
        entry_data = [i for i in cursor.fetchone()]

        data = dict(zip(columns, entry_data))

        cursor.close()

        # self.pick_number = data['pick_number']
        self.pick_round = data['pick_round']
        self.pick_subnumber = data['pick_subnumber']
        self.fantasy_team = data['fantasy_team']
        self.fantasy_team_id = data['team_id']
        self.player_name = data['player_name']
        self.player_pos = data['player_pos']
        self.keeper_indicator = data['keeper_indicator']
        self.fpts = data['FPTS']
        self.nba = data['NBA']
        self.adp = data['AVG']

        return data

    def get_all(self):
        cursor = self.conn.cursor()

        query = '''SELECT * FROM draft_board'''
        df = pd.read_sql(query, self.conn)
        cursor.close()

        return df

    def next_pick(self):
        '''TODO: Alter so that the pick numbers map to rounds based on variable input.
        TODO: Run PostDraftAnalysis.export_results(df). Need to define file path at the start menu.

        Currently hard coded to 12 teams and 14 rounds.'''

        if self.pick_number == 168:
            df = self.get_all()
            # PostDraftAnalysis.export_results(df)

        self.pick_number += 1

        if self.pick_number % 12 != 0:
            self.pick_round = self.pick_number // 12 + 1

        self.pick_subnumber = self.pick_number - 12 * (self.pick_round - 1)

        entry_dict = self.get(self.pick_number)

        if self.keeper_indicator == 1:
            # Post player selection to the draft board
            # entry_dict['player_name'] = self.player_name
            # entry_dict['player_pos'] = self.player_pos
            # entry_dict['player_team'] = self.player_team
            # entry_dict['FPTS'] = fpts
            # entry_dict['AVG'] = avg
            entry_dict['NBA'] = 0 #TODO: Complete individual player's nba calculation
            self.create(entry_dict)
            self.next_pick()
        else:
            return entry_dict

    def previous_pick(self):
        '''TODO: Alter so that the pick numbers map to rounds based on variable input.

        Currently hard coded to 12 teams and 14 rounds.'''

        if self.pick_number != 1:
            self.pick_number -= 1

            if self.pick_number % 12 != 0:
                self.pick_round = self.pick_number // 12 + 1
            else:
                pass

            self.pick_subnumber = self.pick_number - 12 * (self.pick_round - 1)

            if self.keeper_indicator == 1:
                cursor = self.conn.cursor()
                query = cursor.execute('''SELECT FPTS, AVG
                               FROM players
                               WHERE player_name = ? AND player_team = ?''', (self.player_name, self.player_team))  # TODO: Add POS
                query = query.fetchone()
                fpts, avg = query[0], query[1]
                # Post player selection to the draft board
                entry_dict = {}
                entry_dict['pick_number'] = self.pick_number
                entry_dict['player_name'] = self.player_name
                entry_dict['player_pos'] = self.player_pos
                entry_dict['player_team'] = self.player_team
                entry_dict['FPTS'] = fpts
                entry_dict['AVG'] = avg
                entry_dict['NBA'] = 0  # TODO: Complete individual player's nba calculation
                self.create(entry_dict)

                self.next_pick()

    def calculate_nba(self, df):
        '''TODO: Overhaul the NBA calculation system. Preferably, move it to the player class along with the
        get_players method.'''
        if (self.pick_round % 2) == 1:
            next_pick = 12 * (self.pick_round) + (13 - self.pick_subnumber)

        else:
            next_pick = (12 * (self.pick_round + 1) + (13 - self.pick_subnumber)) - 12
        df_next_pick = df[df['AVG'] >= next_pick]

        df['NBA1'] = ''
        df['NBA2'] = ''
        df['NBA3'] = ''
        df['NBA4'] = ''
        df['NBA5'] = ''

        df_next_pick = df[df['AVG'] >= next_pick]
        for pos in ['QB', 'RB', 'WR', 'TE', 'DST']:
            for i in range(1, 6):
                col = 'NBA' + str(i)
                nba = round(df_next_pick[df_next_pick['player_pos'] == pos].FPTS.nlargest(i).iloc[-1], 1)
                df.loc[df['player_pos'] == pos, col] = df.loc[df['player_pos'] == pos, 'FPTS'] - nba

        df.NBA1 = df.NBA1.apply(lambda x: round(x, 1))
        df.NBA2 = df.NBA2.apply(lambda x: round(x, 1))
        df.NBA3 = df.NBA3.apply(lambda x: round(x, 1))
        df.NBA4 = df.NBA4.apply(lambda x: round(x, 1))
        df.NBA5 = df.NBA5.apply(lambda x: round(x, 1))
        return df.sort_values(by='AVG', ascending=False, axis=0)

    def get_players(self, drafted=False):
        '''TODO: This should be moved to a separate class. Leaving it here for now since a presenter can only have
        one model.
        '''

        table_name = 'players'
        cursor = self.conn.cursor()

        if drafted:
            query = f'''SELECT p.player_name, p.player_team, p.FPTS, p.player_pos, p.AVG, p.draft_indicator, db.pick_number
                                FROM players p
                                JOIN draft_board db ON p.player_name = db.player_name
                                WHERE p.draft_indicator = 1
                                ORDER BY db.pick_number
                                '''
            df = pd.read_sql_query(query, self.conn)
            return df
        else:
            query = f'''SELECT players.player_name, players.player_team, players.FPTS, players.player_pos, players.AVG, players.draft_indicator
                                FROM players
                                WHERE players.draft_indicator = 0
                                '''
            df = pd.read_sql_query(query, self.conn)
            df = self.calculate_nba(df)
            return df
