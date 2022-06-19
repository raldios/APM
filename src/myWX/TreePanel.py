import wx
import logging
from pathlib import Path

from myWX.FolderTree import FolderTree
from handlers.DirectoryCrawler import DirectoryCrawler
# from wxClasses.library.TreeMenu import TreeMenu
from helpers import FolderHelpers, FileHelpers


class TreePanel(wx.Panel):

    def __init__(self, parent, data, crawler_queue, tree_edits_queue, db_queue):
        wx.Panel.__init__(self, parent=parent)

        self.data = data
        self.crawler = DirectoryCrawler(data, crawler_queue, tree_edits_queue, db_queue)
        self.crawler_queue = crawler_queue
        self.tree_edits_queue = tree_edits_queue

        self._create_widgets()
        self._create_boxes()
        self._bind_widgets()

        self.tree.start_thread()
        self.crawler.start_thread()

    def _create_widgets(self):
        font_data = wx.Font(wx.FontInfo(12))

        # Create Items ###################
        self.source_choice = wx.Choice(self, choices=self._get_choices())
        self.source_choice.SetSelection(0)

        self.button_refresh = wx.Button(self, label='Refresh', style=wx.BORDER_NONE)
        self.button_open = wx.Button(self, label='Open', style=wx.BORDER_NONE)

        self.count_label = wx.StaticText(self, label='')
        self.size_label = wx.StaticText(self, label='')

        self.count_label.SetFont(font_data)
        self.size_label.SetFont(font_data)

        self.tree: FolderTree = FolderTree(self, self.tree_edits_queue)
        self.crawler_queue.put(self.data.config.sources[self.data.config.default_source])

    def _create_boxes(self):
        archive_box = wx.BoxSizer()
        archive_box.Add(self.source_choice, 1, wx.EXPAND | wx.ALL)
        archive_box.Add(10, 0, 0)
        archive_box.Add(self.button_refresh, 0, wx.EXPAND | wx.ALL)
        archive_box.Add(10, 0, 0)
        archive_box.Add(self.button_open, 0, wx.EXPAND | wx.ALL)

        details_box = wx.BoxSizer()
        details_box.Add(10, 0, 0)
        details_box.Add(self.count_label, 0, wx.EXPAND | wx.ALL)
        details_box.Add(100, 0, 0)
        details_box.Add(self.size_label, 0, wx.EXPAND | wx.ALL)

        tree_box = wx.BoxSizer(wx.VERTICAL)
        tree_box.Add(self.tree, 1, wx.EXPAND | wx.ALL)

        main_box = wx.BoxSizer(wx.VERTICAL)
        main_box.Add(archive_box, 0, wx.EXPAND | wx.ALL, 5)
        main_box.Add(details_box, 0, wx.EXPAND | wx.ALL, 5)
        main_box.Add(tree_box, 1, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(main_box)

    def _bind_widgets(self):
        self.button_refresh.Bind(wx.EVT_BUTTON, self.on_refresh_tree)
        self.button_open.Bind(wx.EVT_BUTTON, self.on_open_source)
        self.source_choice.Bind(wx.EVT_CHOICE, self._on_source_change)
        # self.tree.Bind(wx.EVT_TREE_ITEM_MENU, self._on_tree_item_menu)

    def _blank_source_details(self):
        self.count_label.SetLabel('')
        self.size_label.SetLabel('')

    def update_source_details(self):
        logging.debug('updating details')
        source_zip_count = self.tree.zip_count
        source_folder_size = FileHelpers.format_bytes(self.tree.size)

        zips_text = 'Zips: ' + str(source_zip_count)
        size_text = 'Size: ' + str(source_folder_size)

        self.count_label.SetLabel(zips_text)
        self.size_label.SetLabel(size_text)

    def _get_choices(self):
        choices = []

        for source in self.data.config.sources.values():
            choices.append(source)

        return choices

    def _get_selected_source_path(self):
        index: int = self.source_choice.GetSelection()
        return self.data.config.sources.values()[index]

    def on_open_source(self, event=None):
        selection = self.source_choice.GetSelection()
        path = self.source_choice.GetString(selection)

        FolderHelpers.open_location(Path(path))

    def on_refresh_tree(self, event=None):
        selection = self.source_choice.GetSelection()
        path = self.source_choice.GetString(selection)

        self.crawler_queue.put(path)

    def _on_source_change(self, event=None):
        selection = self.source_choice.GetSelection()
        path = self.source_choice.GetString(selection)

        self.crawler_queue.put(path)

    def _on_tree_item_menu(self, event=None):
        pass
        # item_data = self.tree.GetItemData(event.GetItem())
        # context_menu = TreeMenu(self.data, item_data)
        # self.PopupMenu(context_menu, event.GetPoint())






