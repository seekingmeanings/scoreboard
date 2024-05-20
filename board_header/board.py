
class Board:
    def __init__(self, name, address):
        self.name = name
        self.address = address

        self.io_link: object = None

    def get_board_obj(self):
        return self.io_link