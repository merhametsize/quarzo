import quarto
from quarto import Quarto
from .quarzo import Quarzo
from .minimax import MiniMax
from .montecarlo import MonteCarlo

class QuarzoMiniMax(quarto.Player):
    '''
    Quarzo player. Depending on the number of pawns on the board, the
    minimax depth parameter changes. Late game states allow for more depth.
    '''
    def __init__(self, quarto: Quarto, depthA=1, depthB=3) -> None:
        super().__init__(quarto)
        self.quarzo = Quarzo(quarto)
        self.minimax = MiniMax(self.quarzo)

        self.MINIMAX_INITIAL_DEPTH = depthA
        self.MINIMAX_FINAL_DEPTH = depthB

    def choose_piece(self) -> int:
        self.quarzo.set_board_status()
        num_pawns = self.quarzo.get_num_pawns()
        if num_pawns >= 0 and num_pawns <= 9:
            self.minimax.depth = self.MINIMAX_INITIAL_DEPTH
        else:
            self.minimax.depth = self.MINIMAX_FINAL_DEPTH
        piece = self.minimax.choose_piece()
        # print(f'Nodes visited: {self.minimax.num_nodes_visited}')
        # print(f'Alpha cutoffs: {self.minimax.num_alpha_cut}')
        # print(f'Beta cutoffs: {self.minimax.num_beta_cut}')
        return piece

    def place_piece(self) -> tuple[int, int]:
        self.quarzo.set_board_status()
        num_pawns = self.quarzo.get_num_pawns()
        if num_pawns >= 0 and num_pawns <= 9:
            self.minimax.depth = self.MINIMAX_INITIAL_DEPTH
        else:
            self.minimax.depth = self.MINIMAX_FINAL_DEPTH
        (x, y) = self.minimax.place_piece()
        # print(f'Nodes visited: {self.minimax.num_nodes_visited}')
        # print(f'Alpha cutoffs: {self.minimax.num_alpha_cut}')
        # print(f'Beta cutoffs: {self.minimax.num_beta_cut}')
        return (x, y)

class QuarzoMontecarlo(quarto.Player):
    '''
    Quarzo player. Depending on the number of pawns on the board, the
    montecarlo simulation rate changes. Late game states allow for more simulations.
    '''
    def __init__(self, quarto: Quarto) -> None:
        super().__init__(quarto)
        self.quarzo = Quarzo(quarto)
        self.montecarlo = MonteCarlo(self.quarzo)

        self.MONTECARLO_INITIAL_RATE = 20
        self.MONTECARLO_FINAL_RATE = 50

    def choose_piece(self) -> int:
        self.quarzo.set_board_status()
        num_pawns = self.quarzo.get_num_pawns()
        if num_pawns >= 0 and num_pawns <= 11:
            self.montecarlo.num_matches = self.MONTECARLO_INITIAL_RATE
        else:
            self.montecarlo.num_matches = self.MONTECARLO_FINAL_RATE
        piece = self.montecarlo.choose_piece()
        return piece

    def place_piece(self) -> tuple[int, int]:
        self.quarzo.set_board_status()
        num_pawns = self.quarzo.get_num_pawns()
        if num_pawns >= 0 and num_pawns <= 11:
            self.montecarlo.num_matches = self.MONTECARLO_INITIAL_RATE
        else:
            self.montecarlo.num_matches = self.MONTECARLO_FINAL_RATE
        (x, y) = self.montecarlo.place_piece()
        return (x, y)
