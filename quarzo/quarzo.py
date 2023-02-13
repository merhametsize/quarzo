import copy
import numpy as np

from quarto import Quarto, Piece

class Quarzo():
    '''
    Modified version of the Quarto class. This one allows exploring the state space,
    doing and undoing moves, keeping track of free spots and usable pieces, all
    without altering the game state in the Quarto class.
    '''

    BOARD_SIDE = 4

    def __init__(self, quarto: Quarto) -> None:
        self.quarto = quarto
        self.board = None
        self.binary_board = np.full(shape=(self.BOARD_SIDE, self.BOARD_SIDE, 4), fill_value=np.nan)
        self.pieces = []
        self.current_player = 1
        self.__selected_piece_index = -1

        self.__usable_pieces = []
        self.__free_spots = []
        self.usable_pieces_reset = []
        self.free_spots_reset = []

        self.__create_piece_list()
        self.set_board_status()        
        self.__compute_usable_pieces()
        self.__compute_free_spots()
    
    def set_board_status(self):
        self.board = self.quarto.get_board_status()
        for y in range(self.BOARD_SIDE):
            for x in range(self.BOARD_SIDE):
                piece = self.board[y][x]
                if piece == -1:
                    self.binary_board[y, x][:] = np.nan
                else:
                    self.binary_board[y, x][:] = self.pieces[piece].binary

        self.__selected_piece_index = self.quarto.get_selected_piece()
        self.__compute_usable_pieces()
        self.__compute_free_spots()
    
    def reset_board_status(self):
        '''
        Used in the simulation. Resets the board status to the status before the 
        simulation started.
        '''
        self.__usable_pieces = copy.deepcopy(self.__usable_pieces_reset)
        self.__free_spots = copy.deepcopy(self.__free_spots_reset)
        self.board = self.quarto.get_board_status()
    
    def __compute_usable_pieces(self):
        self.__usable_pieces.clear()
        for i in range(0, 16):
            if i not in self.board:
                self.__usable_pieces.append(i)
        self.__usable_pieces_reset = copy.deepcopy(self.__usable_pieces)

    def __compute_free_spots(self):
        self.__free_spots.clear()
        for x in range(self.BOARD_SIDE):
            for y in range(self.BOARD_SIDE):
                if self.board[y, x] == -1:
                    self.__free_spots.append((x, y))
        self.__free_spots_reset = copy.deepcopy(self.__free_spots)
    
    def switch_player(self):
        self.current_player = self.current_player ^ 1 #bitwise XOR
    
    def __create_piece_list(self):
        self.pieces.append(Piece(False, False, False, False))  # 0
        self.pieces.append(Piece(False, False, False, True))  # 1
        self.pieces.append(Piece(False, False, True, False))  # 2
        self.pieces.append(Piece(False, False, True, True))  # 3
        self.pieces.append(Piece(False, True, False, False))  # 4
        self.pieces.append(Piece(False, True, False, True))  # 5
        self.pieces.append(Piece(False, True, True, False))  # 6
        self.pieces.append(Piece(False, True, True, True))  # 7
        self.pieces.append(Piece(True, False, False, False))  # 8
        self.pieces.append(Piece(True, False, False, True))  # 9
        self.pieces.append(Piece(True, False, True, False))  # 10
        self.pieces.append(Piece(True, False, True, True))  # 11
        self.pieces.append(Piece(True, True, False, False))  # 12
        self.pieces.append(Piece(True, True, False, True))  # 13
        self.pieces.append(Piece(True, True, True, False))  # 14
        self.pieces.append(Piece(True, True, True, True))  # 15
    
    def select(self, pieceIndex: int):
        self.__selected_piece_index = pieceIndex

    def place(self, x: int, y: int):
        self.board[y, x] = self.__selected_piece_index
        self.binary_board[y, x][:] = self.pieces[self.__selected_piece_index].binary
        self.__usable_pieces.remove(self.__selected_piece_index)
        self.__free_spots.remove((x, y))
    
    def unplace(self, x: int, y: int):
        piece = self.board[y, x]
        self.__usable_pieces.append(piece)
        self.__free_spots.append((x, y))
        self.board[y, x] = -1
        self.binary_board[y, x][:] = np.nan
    
    def __check_horizontal(self) -> int:
        hsum = np.sum(self.binary_board, axis=1)

        if self.BOARD_SIDE in hsum or 0 in hsum:
            return self.current_player
        else:
            return -1

    def __check_vertical(self):
        vsum = np.sum(self.binary_board, axis=0)

        if self.BOARD_SIDE in vsum or 0 in vsum:
            return self.current_player
        else:
            return -1

    def __check_diagonal(self):
        dsum1 = np.trace(self.binary_board, axis1=0, axis2=1)
        dsum2 = np.trace(np.fliplr(self.binary_board), axis1=0, axis2=1)

        if self.BOARD_SIDE in dsum1 or self.BOARD_SIDE in dsum2 or 0 in dsum1 or 0 in dsum2:
            return self.current_player
        else:
            return -1
    
    def check_winner(self) -> int:
        l = [self.__check_horizontal(), self.__check_vertical(), self.__check_diagonal()]
        for elem in l:
            if elem >= 0:
                return elem
        return -1

    def check_finished(self) -> bool:
        for row in self.board:
            for elem in row:
                if elem == -1:
                    return False
        return True
    
    @property
    def free_spots(self):
        return copy.deepcopy(self.__free_spots)
    
    @property
    def usable_pieces(self):
        return copy.deepcopy(self.__usable_pieces)
    
    def get_selected_piece(self):
        return copy.deepcopy(self.__selected_piece_index)
    
    def get_num_pawns(self):
        return (self.board >= 0).sum()