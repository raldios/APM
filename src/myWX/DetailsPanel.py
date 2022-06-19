import wx
import logging

from pathlib import Path
from helpers import DazHelpers, FileHelpers, FolderHelpers


class DetailsPanel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)

        self._create_widgets()
        self._create_boxes()

    def _create_widgets(self):
        font_title = wx.Font(wx.FontInfo(16))

        self.title = wx.StaticText(self, label='')
        self.title.SetFont(font_title)

        body_style = wx.TextAttr()
        body_style.SetFontSize(16)
        self.body = wx.TextCtrl(self, value='', style=wx.TE_MULTILINE | wx.TE_READONLY |
                                                      wx.SUNKEN_BORDER | wx.TE_DONTWRAP)
        self.body.SetDefaultStyle(body_style)

    def _create_boxes(self):
        main_box = wx.BoxSizer(wx.VERTICAL)
        main_box.Add(self.title, 0, wx.EXPAND | wx.ALL, 5)
        main_box.Add(self.body, 1, wx.EXPAND | wx.ALL, 5)
        main_box.Add(0, 0, 3)

        self.SetSizer(main_box)

    def set_body_text(self, event, tree):
        # switch to retrieve from db
        path = tree.GetItemData(event.GetItem())
        installed = False

        if path.is_dir():
            self.body.SetLabelText('')
            self.title.SetLabelText(path.name)
            self.body.WriteText(f'Path:\t\t{path}\n\n')
            size = FolderHelpers.get_folder_size(path)
            self.body.WriteText(f'Size:\t\t{FileHelpers.format_bytes(size)}\n')
            self.body.WriteText(f'Zip Count:\t{FolderHelpers.get_zip_count(path)}\n')
        else:
            self.body.SetLabelText('')
            self.title.SetLabelText(DazHelpers.parse_product_name(path))
            self.body.WriteText(f'Folder:\t\t{path.parent}\n')
            self.body.WriteText(f'Filename:\t\t{path.name}\n')
            size = FileHelpers.get_file_size(path)
            self.body.WriteText(f'Size:\t\t{FileHelpers.format_bytes(size)}\n')
            self.body.WriteText(f'SKU:\t\t{DazHelpers.get_sku(path)}\n')
            self.body.WriteText(f'Installed: \t\t{installed}')

