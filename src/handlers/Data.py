from handlers.Config import ConfigHandler


class DataHandler:

    def __init__(self):

        self.config = ConfigHandler()

        if self.config.critical is True:
            return