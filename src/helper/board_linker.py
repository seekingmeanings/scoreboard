from src.board import BoardConfig


class BoardLinker:
    """
    this class makes linking content outside of other classe
    """

    def __init__(self, board: BoardConfig) -> None:
        """
        its just board atm, could be extended
        :param board:
        """
        self.board = board
