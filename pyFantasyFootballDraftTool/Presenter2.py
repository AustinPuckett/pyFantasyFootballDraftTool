import csv
import os
import tkinter.filedialog
import tkinter as tk
import PostDraftAnalysis

from View import *


class ImportDataPresenter():
    def __init__(self, master, model, view):
        self.master = master
        self.model = model
        self.view = view

    def start_draft(self, event):
        self.model.create_draft_tables()
        self.master.change_view(DraftRoomView)

    def exit_draft(self, event):
        self.view.grid_forget()

    def import_adp(self, event):
        upload_file = tk.filedialog.askopenfilename()
        self.model.create_adp_table(upload_file)
        self.view.import_adp_status.config(text='Success!')

    def import_projections(self, event):
        upload_file = tk.filedialog.askopenfilename()
        self.model.create_projections_table(upload_file)
        self.view.import_projections_status.config(text='Success!')

    def import_draft(self, event):
        upload_file = tk.filedialog.askopenfilename()
        self.model.create_draft_table(upload_file)
        self.view.import_draft_order_status.config(text='Success!')

    def run(self):
        self.view.init_ui(self)
        self.view.grid()

    def exit_view(self):
        self.view.grid_forget()


class DraftRoomPresenter():
    def __init__(self, master, model, view):
        self.master = master
        self.model = model
        self.view = view

    def select_player(self, event=None):
        tree_entry_id = self.view.tree.focus()

        tree_entry_vals = self.view.tree.item(tree_entry_id)['values']
        tree_entry_dict = dict(zip(self.tree_columns, tree_entry_vals))

        self.clear_pick(None)

        self.view.player_id.config(text='None')
        self.view.player_name.config(text=tree_entry_dict['player_name'])
        self.view.player_team.config(text=tree_entry_dict['player_team'])
        self.view.player_position.config(text=tree_entry_dict['player_pos'])

        # self.view.player_id.config(text=tree_entry_dict[''])
        # self.view.player_name.config(text=tree_entry_dict[''])
        # self.view.player_team.config(text=tree_entry_dict[''])
        # self.view.player_position.config(text=tree_entry_dict[''])

    def submit_pick(self, event):
        tree_entry_id = self.view.tree.focus()
        tree_entry_vals = self.view.tree.item(tree_entry_id)['values']
        tree_entry_dict = dict(zip(self.tree_columns, tree_entry_vals))

        pick_round = self.view.pick_round.cget('text')
        pick_subnumber = self.view.pick_subnumber.cget('text')
        pick_number = self.view.pick_subnumber.cget('text')
        player_name = self.view.player_name.cget('text')
        player_pos = self.view.player_position.cget('text')
        player_team = self.view.player_team.cget('text')
        fpts = tree_entry_dict['FPTS']
        nba = tree_entry_dict['NBA1']
        avg = tree_entry_dict['AVG']

        pick_entry = {'pick_number': pick_number,
                      'player_name': player_name,
                      'player_pos': player_pos,
                      'player_team': player_team,
                      'FPTS': fpts,
                      'NBA': nba,
                      'AVG': avg,
                      }
        self.model.create(pick_entry)
        self.model.next_pick()
        self.clear_pick(event=None)
        self.run()

    def show_tree_menu(self, event):
        # Retrieve selected item from treeview
        item = self.view.tree.focus()

        # If item is selected, display context menu
        if item:
            self.view.tree_menu.post(event.x_root, event.y_root)

    def instantiate_tree(self):
        df = self.model.get_players()
        self.tree_columns = list(df.columns)
        self.view.tree.config(columns=self.tree_columns, selectmode='browse')

        for col in self.tree_columns:
            self.view.tree.column(col, minwidth=0, width=110, stretch=False)
            self.view.tree.heading(col, text=col.title())

    def load_tree_entries(self):
        df = self.model.get_players()
        for item in self.view.tree.get_children():
            self.view.tree.delete(item)

        for row in df.values:
            self.view.tree.insert('', 0, values=list(row))
        # self.view.grid(row=0, column=0, padx=1, pady=2)

    # def show_start_view(self, event):
    #     self.master.change_view(StartView)

    def run(self):
        self.view.init_ui(self)

        self.instantiate_tree()
        self.load_tree_entries()

        self.view.pick_subnumber.config(text=self.model.pick_subnumber)
        self.view.pick_number.config(text=self.model.pick_number)
        self.view.pick_round.config(text=self.model.pick_round)
        self.view.fantasy_team.config(text=self.model.get(self.model.pick_number)['fantasy_team'])

        self.view.grid()

    def clear_pick(self, event):
        pass
        # self.view.id_entry.configure(text='')
        # self.view.date_entry.delete(0, 'end')
        # self.view.exercise_entry.delete(0, 'end')
        # self.view.workout_type_entry.delete(0, 'end')
        # self.view.workout_class_entry.delete(0, 'end')
        # self.view.measure_entry.config(text='')
        # self.view.value_entry.delete(0, 'end')
        # self.view.reps_entry.delete(0, 'end')

    def exit_draft(self, event):
        self.view.grid_forget()

    def draft_board(self, event):
        self.master.change_view(DraftBoardView)

    def prior_pick(selfself, event):
        self.model.previous_pick()
        self.run()

    def exit_view(self):
        self.view.grid_forget()


class DraftBoardPresenter():
    def __init__(self, master, model, view):
        self.master = master
        self.model = model
        self.view = view

    def instantiate_tree(self):
        df = self.model.get_players(drafted=True)
        self.tree_columns = list(df.columns)
        self.view.tree.config(columns=self.tree_columns, selectmode='browse')

        for col in self.tree_columns:
            self.view.tree.column(col, minwidth=0, width=110, stretch=False)
            self.view.tree.heading(col, text=col.title())

    def load_tree_entries(self):
        df = self.model.get_players(drafted=True)
        for item in self.view.tree.get_children():
            self.view.tree.delete(item)

        for row in df.values:
            self.view.tree.insert('', 0, values=list(row))
        # self.view.grid(row=0, column=0, padx=1, pady=2)

    def run(self):
        self.view.init_ui(self)

        self.instantiate_tree()
        self.load_tree_entries()

        self.view.grid()

    def draft_room(self, event):
        self.master.change_view(DraftRoomView)

    def exit_view(self):
        self.view.grid_forget()