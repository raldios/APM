import wx
import logging
from queue import Queue
from helpers import DazHelpers

from handlers.Data import DataHandler

from myWX.MenuBar import MenuBar
from myWX.LibraryNotebook import LibraryNotebook
from myWX.DetailsPanel import DetailsPanel


class AssetPackageManagerFrame(wx.Frame):

    def __init__(self, parent, wx_id, title):

        wx.Frame.__init__(self, parent, wx_id, title,
                          pos=wx.DefaultPosition,
                          size=(1100, 800),
                          style=wx.DEFAULT_FRAME_STYLE)

        self.data: DataHandler = DataHandler()
        if self.data.config.critical:
            logging.critical('APM Has experienced a critical error during data initialization and must exit')
            self.Close()
            return
#
        logging.info('--- APM Started ---------------')

        self.crawler_queue = Queue()
        self.tree_edits_queue = Queue()
        self.db_queue = Queue()

        self.main_splitter = None
        self.library_notebook = None
        self.tree_panel = None
        self.olv_panel = None

        self._create_body()

    def _create_body(self):
        logging.debug('Creating APM main frame')
        self.menu_bar = MenuBar()
        self.SetMenuBar(self.menu_bar)
        self._create_main_splitter()
        self._create_binds()

    def _create_main_splitter(self):
        logging.debug("Creating main_splitter")
        self.main_splitter = wx.SplitterWindow(self)
        self.main_splitter.SetSashGravity(0.5)
        self.main_splitter.SetSashInvisible(True)

        self.notebook_panel: LibraryNotebook = LibraryNotebook(self.main_splitter, self.data,
                                                               self.crawler_queue, self.tree_edits_queue, self.db_queue)

        # todo make a new DetailsPanel to implement
        self.details_panel: DetailsPanel = DetailsPanel(self.main_splitter)

        self.main_splitter.SplitVertically(self.notebook_panel, self.details_panel)
        logging.debug("Finished main_splitter")

    def _create_binds(self):
        tree = self.notebook_panel.tree_panel.tree

        DazHelpers.better_bind(self, wx.EVT_TREE_SEL_CHANGED, tree, self.details_panel.set_body_text, tree)
