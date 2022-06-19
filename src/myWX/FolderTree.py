import logging
import wx
from pathlib import Path
from threading import *

from helpers import FileHelpers, DazHelpers


class FolderTree(wx.TreeCtrl):

    def __init__(self, parent, tree_edits_queue,
                 wx_id=wx.ID_ANY, position=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE):

        wx.TreeCtrl.__init__(self, parent, wx_id, position, size, style)

        self.parent = parent
        self.tree_edits_queue = tree_edits_queue
        self.nodes = dict()
        self.tree_nodes = dict()

        self.root_path = None
        self.zip_count = 0
        self.size = 0

        self.AssignImageList(self.create_image_list())

    def start_thread(self):
        thread = Thread(target=self.queue_loop)
        thread.start()

    def queue_loop(self):
        while True:
            nodes, root_path = self.tree_edits_queue.get()
            self.parent.Disable()
            self.make_from_dict(nodes, root_path)
            self.parent.Enable()

    def make_from_dict(self, new_nodes: dict, root_path):

        if root_path != self.root_path:
            self.root_path = root_path
            self.tree_nodes = dict()
            self.nodes = dict()
            self.DeleteAllItems()
            self.size = 0
            self.zip_count = 0
            logging.debug('root_path changed, tree reset')

        elif self.nodes.keys() == new_nodes.keys():
            logging.debug('new_nodes == self.nodes, no edit to tree')
            return

        new_tree_nodes = dict()

        for key, value in new_nodes.items():
            if key in self.tree_nodes.keys():
                new_tree_nodes[key] = self.tree_nodes[key]

            elif value['parent'] is not None:
                parent_key = str(value['parent'])

                parent = new_tree_nodes[parent_key]
                path = Path(key)
                if not path.is_dir():
                    # name = DazHelpers.parse_product_name(path)
                    name = value['name']
                else:
                    name = value['name']
                image = 0 if Path(key).is_dir() else 1

                if path.suffix == '.zip':
                    self.zip_count += 1
                    self.size += FileHelpers.get_file_size(path)

                new_tree_nodes[key] = self.AppendItem(parent, name, data=path, image=image)

            elif self.IsEmpty() and value['parent'] is None:
                name = Path(key).name
                new_tree_nodes[key] = self.AddRoot(name)

        for key, value in self.nodes.items():
            if key not in new_nodes.keys():
                self.Delete(self.tree_nodes[key])

        self.nodes = new_nodes
        self.tree_nodes = new_tree_nodes
        for key, value in self.tree_nodes.items():
            self.SortChildren(value)

        self.parent.update_source_details()

    def OnCompareItems(self, item1, item2):
        text1 = self.GetItemText(item1)
        text2 = self.GetItemText(item2)
        is_dir1 = self.GetItemData(item1).is_dir()
        is_dir2 = self.GetItemData(item2).is_dir()

        if (is_dir1 and is_dir2) and text1 < text2:
            return -1
        elif (is_dir1 and is_dir2) and text1 == text2:
            return 0
        elif is_dir1 and is_dir2:
            return 1
        elif is_dir1 and not is_dir2:
            return -1
        elif not is_dir1 and is_dir2:
            return 1
        elif text1 < text2:
            return -1
        elif text1 == text2:
            return 0
        else:
            return 1

    @staticmethod
    def create_image_list():
        logging.debug('creating image list for tree')
        image_list = wx.ImageList(18, 18)

        bitmap_directory = wx.Bitmap(r'0_directory_18.png', wx.BITMAP_TYPE_ANY)
        bitmap_zip = wx.Bitmap(r'1_zip_18.png', wx.BITMAP_TYPE_ANY)

        image_list.Add(bitmap_directory)
        image_list.Add(bitmap_zip)

        return image_list
