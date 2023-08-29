import tkinter as tk
from tkinter import ttk, font
import sqlite3 as sql

from PostDraftAnalysis import generate_draft_report
from View import *
from Model2 import *
from Presenter2 import *



class AppController(tk.Tk):
    '''
    TODO: Menu bar will appear on the Login menu when it should not.
    '''
    def __init__(self):
        super().__init__()

        # TODO: move root and root frame outside of the controller
        self.container = tk.Frame(self)

        self.title('Fantasy Football Draft Tool')

        self.container.grid(row=0, column=0, padx=2, pady=2, ipadx=0, ipady=0, sticky='N')

        self.views = {ImportDataView: {'model': ImportDataModel, 'presenter': ImportDataPresenter},
                        DraftRoomView: {'model': DraftRoomModel, 'presenter': DraftRoomPresenter},
                      DraftBoardView: {'model': DraftRoomModel, 'presenter': DraftBoardPresenter},}

        # db_name = 'draft_db.db'
        db_name = ':memory:'
        self.db_conn = sql.connect(db_name)
        self.active_presenter = None
        self.active_view = None
        self.active_model = None

        self.draft_model = self.views[DraftRoomView]['model'](self.db_conn)

        self.change_view(ImportDataView)

    def change_view(self, view):
        presenter = self.views[view]['presenter']

        # instantiate model
        if self.active_presenter is not None:
            self.active_presenter.exit_view()
            self.active_model = self.draft_model
        else:
            model = self.views[view]['model']
            self.active_model = model(self.db_conn)

        self.geometry('') # Reset root window geometry

        # Instantiate view and presenter
        self.active_view = view(self.container)
        self.active_presenter = presenter(self, self.active_model, self.active_view)

        self.active_presenter.run()

    def close_app(self):
        self.db_conn.close()

