import wx
import logging

from handlers.Data import DataHandler


class MainFrame(wx.Frame):

    def __init__(self, parent, wx_id, title):

        wx.Frame.__init__(self, parent, wx_id, title,
                          pos=wx.DefaultPosition,
                          size=(1100, 800),
                          style=wx.DEFAULT_FRAME_STYLE)

        self.data: DataHandler = DataHandler()
        if self.data.config.critical:
            logging.critical('ADI Has experienced a critical error during data initialization and must exit')
            return
#
        logging.info('--- ADI Started ---------------')

        self.main_splitter = None
        self.notebook_library = None
        self.tree_panel = None
        self.olv_panel = None