from processes.recognizer import Recognizer


class Grid:

    def __init__(self, identifier):
        self.identifier = identifier
        self.__find_grid_entry()

    def __find_grid_entry(self):
        return Recognizer(self.identifier, None).center_of()
