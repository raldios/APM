import logging

from pathlib import Path
from queue import Queue
from threading import *

from handlers.Data import DataHandler

import pickle


class DirectoryCrawler:

    def __init__(self, data, crawler_queue, tree_edit_queue, db_queue):

        self.nodes = dict()
        self.crawler_queue: Queue = crawler_queue
        self.tree_edit_queue: Queue = tree_edit_queue
        self.db_queue = db_queue
        self.valid_files = ['.zip']

        self.zip_count = 0
        self.size = 0

    def print(self):
        for key, value in self.nodes.items():
            print(f'{value} - {key}')

    def start_thread(self):
        thread = Thread(target=self.queue_loop)
        thread.start()

    def queue_loop(self):
        while True:
            root_path = self.crawler_queue.get()
            self.nodes = {str(root_path): {'parent': None}}

            self.tree_edit_queue.put(self.crawl_path(root_path))

    def crawl_path(self, root_path):
        root_path = Path(root_path)
        sub_path_list = [x for x in root_path.iterdir()]

        for sub_path in sub_path_list:

            if str(sub_path) in self.nodes:
                continue
            elif sub_path.is_dir():
                key = str(sub_path)
                parent_path = sub_path.parent
                name = sub_path.name

                self.nodes[key] = {'parent': parent_path, 'name': name}

            elif sub_path.suffix in self.valid_files:
                key = str(sub_path)
                parent_path = sub_path.parent
                name = sub_path.name

                self.nodes[key] = {'parent': parent_path, 'name': name}

            if sub_path.is_dir():
                self.crawl_path(sub_path)

        return self.nodes, root_path
