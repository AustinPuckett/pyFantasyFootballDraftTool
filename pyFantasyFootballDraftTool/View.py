import tkinter as tk
from tkinter import ttk, font


class StartView(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent

    def init_ui(self, presenter):
        # Widget settings
        title_font = font.Font(family='Segoe UI', size=15, weight='bold')
        label_font = font.Font(family='Segoe UI', size=12, weight='bold')
        entry_font = font.Font(family='Segoe UI', size=11, weight='normal')
        button_font = font.Font(family='Segoe UI', size=11, weight='normal')

        # Instantiate widgets
        self.title_text = ttk.Label(self, text='Welcome to the 2023 Draft', font=title_font)
        self.body_text = ttk.Label(self, text='Here is the welcome message.', font=entry_font)
        self.start_button = ttk.Button(self, text='Start')


        # Place widgets
        self.title_text.grid(row=0, column=0, pady=15, columnspan=2, sticky='N')
        # self.login_label.grid(row=0, column=1)
        self.body_text.grid(row=1, column=0, sticky='W', padx=2, pady=1)
        self.start_button.grid(row=2, column=0, sticky='E', padx=2, pady=1)

        # Presenter Bindings
        self.start_button.bind('<Button-1>', presenter.start)


class ImportDataView(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent

    def init_ui(self, presenter):
        # Widget settings
        title_font = font.Font(family='Segoe UI', size=15, weight='bold')
        label_font = font.Font(family='Segoe UI', size=12, weight='bold')
        entry_font = font.Font(family='Segoe UI', size=11, weight='normal')
        button_font = font.Font(family='Segoe UI', size=11, weight='normal')

        # Instantiate widgets
        self.title_text = ttk.Label(self, text='Import Draft Data', font=title_font)
        # self.login_label = ttk.Label(self, text='Login', font=label_font)
        self.body_text = ttk.Label(self, text='Put some info here.', font=entry_font)

        self.import_adp_text = ttk.Label(self, text='ADP Data:', font=entry_font)
        self.import_projections_text = ttk.Label(self, text='Player Projections:', font=entry_font)
        self.import_draft_order_text = ttk.Label(self, text='Draft Order:', font=entry_font)

        self.import_adp_status = ttk.Label(self, text=' Incomplete', font=entry_font)
        self.import_projections_status = ttk.Label(self, text=' Incomplete', font=entry_font)
        self.import_draft_order_status = ttk.Label(self, text=' Incomplete', font=entry_font)

        self.import_adp_button = ttk.Button(self, text='Import ADPs')
        self.import_projections_button = ttk.Button(self, text='Import Player Projections')
        self.import_draft_order_button = ttk.Button(self, text='Import Draft Order')

        self.start_button = ttk.Button(self, text='Begin Draft')
        self.exit_button = ttk.Button(self, text='Exit')

        # Place widgets
        self.title_text.grid(row=0, column=1, pady=15, columnspan=1, sticky='N')

        self.body_text.grid(row=1, column=1, pady=10, columnspan=1, sticky='N')

        self.import_adp_text.grid(row=2, column=0, pady=1, columnspan=1, sticky='N')
        self.import_projections_text.grid(row=3, column=0, pady=1, columnspan=1, sticky='N')
        self.import_draft_order_text.grid(row=4, column=0, pady=1, columnspan=1, sticky='N')

        self.import_adp_status.grid(row=2, column=1, pady=1, columnspan=1, sticky='N')
        self.import_projections_status.grid(row=3, column=1, pady=1, columnspan=1, sticky='N')
        self.import_draft_order_status.grid(row=4, column=1, pady=1, columnspan=1, sticky='N')

        self.import_adp_button.grid(row=5, column=0, pady=1, columnspan=1, sticky='N')
        self.import_projections_button.grid(row=5, column=1, pady=1, columnspan=1, sticky='N')
        self.import_draft_order_button.grid(row=5, column=2, pady=1, columnspan=1, sticky='N')
        
        self.start_button.grid(row=6, column=1, pady=1, columnspan=1, sticky='N')
        self.exit_button.grid(row=6, column=2, pady=1, columnspan=1, sticky='N')

        # Presenter Bindings
        self.import_adp_button.bind('<Button-1>', presenter.import_adp)
        self.import_projections_button.bind('<Button-1>', presenter.import_projections)
        self.import_draft_order_button.bind('<Button-1>', presenter.import_draft)

        self.start_button.bind('<Button-1>', presenter.start_draft)
        self.exit_button.bind('<Button-1>', presenter.exit_draft)


class DraftRoomView(tk.Frame):
    """The window where a user may enter a workout into the database.

    """

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent

    def init_ui(self, presenter):
        # Widget settings
        title_font = font.Font(family='Segoe UI', size=18, weight='bold')
        header_font = font.Font(family='Segoe UI', size=15, weight='bold')
        label_font = font.Font(family='Segoe UI', size=12, weight='bold')
        entry_font = font.Font(family='Segoe UI', size=11, weight='normal')
        button_font = font.Font(family='Segoe UI', size=11, weight='normal')

        # Frame1
        self.frame1 = tk.Frame(self)
        self.title_text = ttk.Label(self.frame1, text='Available Players by NBA', font=title_font, anchor='center')
        self.tree = ttk.Treeview(self.frame1, show="headings")
        self.title_text.grid(row=0, column=0, sticky="NSEW")
        self.tree.grid(row=1, column=0, sticky="NSEW")

        self.tree_menu = tk.Menu(self.frame1, tearoff=0)
        self.tree_menu.add_command(label="Select", command=lambda: presenter.select_player())

        # Frame1 Presenter Bindings
        # self.tree.bind('<Button-1>', presenter.show_tree_menu)
        self.tree.bind('<Double-Button-1>', presenter.select_player)
        # Frame2
        self.frame2 = tk.Frame(self)

        # Create Widgets
        self.frame2_header_text = ttk.Label(self.frame2, text='Draft Player', font=header_font)
        self.player_id = ttk.Label(self.frame2, text='', font=entry_font)
        self.player_name = ttk.Label(self.frame2, text='', font=entry_font)
        self.player_team = ttk.Label(self.frame2, text='', font=entry_font)
        self.player_position = ttk.Label(self.frame2, text='', font=entry_font)
        self.pick_number = ttk.Label(self.frame2, text='', font=entry_font)
        self.pick_round = ttk.Label(self.frame2, text='', font=entry_font)
        self.pick_subnumber = ttk.Label(self.frame2, text='', font=entry_font)
        self.fantasy_team = ttk.Label(self.frame2, text='', font=entry_font)
        # self.fpts = None
        # self.nba = None
        # self.avg = None

        self.player_id_text = ttk.Label(self.frame2, text='Player ID: ', font=entry_font)
        self.player_name_text = ttk.Label(self.frame2, text='Player Name:', font=entry_font)
        self.player_team_text = ttk.Label(self.frame2, text='Team: ', font=entry_font)
        self.player_position_text = ttk.Label(self.frame2, text='Position: ', font=entry_font)
        self.pick_number_text = ttk.Label(self.frame2, text='Cumulative Pick No: ', font=entry_font)
        self.pick_round_text = ttk.Label(self.frame2, text='Round: ', font=entry_font)
        self.pick_subnumber_text = ttk.Label(self.frame2, text='Pick No: ', font=entry_font)
        self.fantasy_team_text = ttk.Label(self.frame2, text='Fantasy Team', font=entry_font)

        # Place entry and text widgets
        self.frame2_header_text.grid(row=0, column=2, pady=15, columnspan=2, sticky='W')

        
        self.pick_round_text.grid(row=1, column=0, sticky='E', padx=2, pady=1)
        self.pick_subnumber_text.grid(row=2, column=0, sticky='E', padx=2, pady=1)
        self.fantasy_team_text.grid(row=3, column=0, sticky='E', padx=2, pady=1)

        self.pick_round.grid(row=1, column=1, sticky='W', padx=2, pady=1)
        self.pick_subnumber.grid(row=2, column=1, sticky='W', padx=2, pady=1)
        self.fantasy_team.grid(row=3, column=1, sticky='W', padx=2, pady=1)
        
        self.player_id_text.grid(row=1, column=2, sticky='E', padx=2, pady=1)
        self.player_name_text.grid(row=2, column=2, sticky='E', padx=2, pady=1)
        self.player_position_text.grid(row=3, column=2, sticky='E', padx=2, pady=1)
        self.player_team_text.grid(row=4, column=2, sticky='E', padx=2, pady=1)


        self.player_id.grid(row=1, column=3, sticky='E', padx=2, pady=1)
        self.player_name.grid(row=2, column=3, sticky='E', padx=2, pady=1)
        self.player_position.grid(row=3, column=3, sticky='E', padx=2, pady=1)
        self.player_team.grid(row=4, column=3, sticky='E', padx=2, pady=1)
        
        # Frame3
        self.frame3 = tk.Frame(self)
        self.button_submit = ttk.Button(self.frame3, text='Submit')
        self.button_exit = ttk.Button(self.frame3, text='Exit')
        self.button_clear = ttk.Button(self.frame3, text='Clear')
        self.button_draft_board = ttk.Button(self.frame3, text='Draft Board')

        self.button_exit.grid(row=0, column=0, sticky='S', padx=2, pady=5)
        self.button_clear.grid(row=0, column=1, sticky='S', padx=2, pady=5)
        self.button_submit.grid(row=0, column=2, sticky='S', padx=2, pady=5)
        self.button_draft_board.grid(row=0, column=4, sticky='S', padx=10, pady=5)

        self.button_submit.bind('<Button-1>', presenter.submit_pick)
        self.button_exit.bind('<Button-1>', presenter.exit_draft)
        self.button_clear.bind('<Button-1>', presenter.clear_pick)
        self.button_draft_board.bind('<Button-1>', presenter.draft_board)

        # Frame placements
        self.frame1.grid(row=0, column=0, padx=10, pady=2)
        self.frame2.grid(row=1, column=0, padx=1, pady=5, sticky="NSEW")
        self.frame3.grid(row=2, column=0, padx=1, pady=5, sticky="NSEW")


class DraftBoardView(tk.Frame):
    """The window where a user may enter a workout into the database.

    """

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent

    def init_ui(self, presenter):
        # Widget settings
        title_font = font.Font(family='Segoe UI', size=18, weight='bold')
        header_font = font.Font(family='Segoe UI', size=15, weight='bold')
        label_font = font.Font(family='Segoe UI', size=12, weight='bold')
        entry_font = font.Font(family='Segoe UI', size=11, weight='normal')
        button_font = font.Font(family='Segoe UI', size=11, weight='normal')

        # Frame1
        self.frame1 = tk.Frame(self)
        self.title_text = ttk.Label(self.frame1, text='Drafted Players', font=title_font, anchor='center')
        self.tree = ttk.Treeview(self.frame1, show="headings")
        self.title_text.grid(row=0, column=0, sticky="NSEW")
        self.tree.grid(row=1, column=0, sticky="NSEW")

        self.tree_menu = tk.Menu(self.frame1, tearoff=0)
        # self.tree_menu.add_command(label="Select", command=lambda: presenter.select_player())

        # Frame1 Presenter Bindings

        # Frame
        self.frame2 = tk.Frame(self)
        self.button_exit = ttk.Button(self.frame2, text='Home')
        self.button_exit.grid(row=0, column=0, sticky='S', padx=2, pady=5)
        self.button_exit.bind('<Button-1>', presenter.draft_room)

        # Frame placements
        self.frame1.grid(row=0, column=0, padx=10, pady=2)
        self.frame2.grid(row=2, column=0, padx=1, pady=5, sticky="NSEW")
