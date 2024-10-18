from src.things.scoreboard.scoreboard import Scoreboard


class BoardLinker:
    """
    this class makes linking content outside of other classe
    """

    def __init__(self, board: Scoreboard) -> None:
        """
        its just board atm, could be extended
        :param board:
        """
        self.board = board
