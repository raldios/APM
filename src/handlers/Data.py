from threading import Thread

from handlers.Config import ConfigHandler
from mySQL.Assets import Assets
from mySQL.Folders import Folders


class DataHandler:

    def __init__(self):

        self.config = ConfigHandler()

        if self.config.critical is True: return

        self.assets = Assets()
        self.folders = Folders()

    def start_thread(self):
        thread = Thread(target=self.queue_loop)
        thread.start()

    def queue_loop(self):
        while True:
            instruction = 1