import random
from .quarzo import Quarzo

class MiniMax():
    def __init__(self, quarzo: Quarzo):
        self.quarzo = quarzo
        self.depth = 2
        self.num_alpha_cut = 0
        self.num_beta_cut = 0
        self.num_nodes_visited = 0
    
    def choose_piece(self) -> int:
        '''
        For each available piece, min() is called to simulate the opponent's
        turn. The piece that yielded the highest score is returned.
        ''' 
        usable_pieces = self.quarzo.usable_pieces
        random.shuffle(usable_pieces)
        piece_score_dict = {key: -1 for key in usable_pieces}

        for current_depth in range(self.depth):
            ordered_pieces = [item[0] for item in sorted(piece_score_dict.items(), key=lambda x:-x[1])]
            for p in ordered_pieces:
                self.quarzo.select(p)
                s = self.min_move(alpha=-1, beta=1, depth=current_depth)

                piece_score_dict[p] = s
        return max(piece_score_dict, key=lambda x: piece_score_dict[x]) #Best move
    
    def place_piece(self) -> tuple[int, int]:
        '''
        For each available move, max_piece() is called to choose a piece for the
        opponent. The move that yielded the highest score is returned.
        '''
        free_spots = self.quarzo.free_spots
        random.shuffle(free_spots)
        move_score_dict = {key: -1 for key in free_spots}

        for current_depth in range(self.depth):
            ordered_moves = [item[0] for item in sorted(move_score_dict.items(), key=lambda x:-x[1])]
            for (x, y) in ordered_moves:
                self.quarzo.place(x, y)
                self.num_nodes_visited += 1

                if self.quarzo.check_winner() != -1:
                    score = 1   #QuarzoAI's victory
                elif current_depth == 0:
                    score = 0   #Depth constraint, dummy draw-score returned
                elif self.quarzo.check_finished():
                    score = 0   #Draw
                else:
                    score = self.max_piece(alpha=-1, beta=1, depth=current_depth)
                
                move_score_dict[(x, y)] = score
                    
                self.quarzo.unplace(x, y)
        return max(move_score_dict, key=lambda x: move_score_dict[x]) #Best move
    
    def max_piece(self, alpha=-1, beta=1, depth=1):
        '''
        Picks the piece with the highest yielded score
        '''
        best_score = -100
        for p in self.quarzo.usable_pieces:
            self.quarzo.select(p)
            s = self.min_move(alpha=alpha, beta=beta, depth=depth-1)
            best_score = max(best_score, s)
            alpha = max(alpha, best_score)
            if beta <= alpha:
                self.num_alpha_cut += 1
                break #pruning, alpha cutoff
        return best_score
    
    def min_piece(self, alpha=-1, beta=1, depth=1):
        '''
        Picks the piece with the lowest yielded score
        '''
        best_score = 100
        for p in self.quarzo.usable_pieces:
            self.quarzo.select(p)
            s = self.max_move(alpha=alpha, beta=beta, depth=depth-1)
            best_score = min(best_score, s)
            beta = min(beta, best_score)
            if beta <= alpha:
                self.num_beta_cut += 1
                break #pruning, beta cutoff
        return best_score
    
    def min_move(self, alpha=-1, beta=1, depth=1):
        '''
        Picks the move with the lowest yielded score
        '''
        best_score = 100

        for (x, y) in self.quarzo.free_spots:
            self.quarzo.place(x, y)
            self.num_nodes_visited += 1

            if self.quarzo.check_winner() != -1:
                score = -1  #Opponent's victory
            elif depth == 0:
                score = 0   #Depth constraint, dummy draw-score returned
            elif self.quarzo.check_finished():
                score = 0   #Draw
            else:
                score = self.min_piece(alpha=alpha, beta=beta, depth=depth)

            self.quarzo.unplace(x, y)

            best_score = min(best_score, score)
            beta = min(beta, best_score)
            if beta <= alpha:
                self.num_beta_cut += 1
                break #pruning, beta cutoff
        return best_score
    
    def max_move(self, alpha=-1, beta=1, depth=1):
        '''
        Picks the move with the highest yielded score
        '''
        best_score = -100

        for (x, y) in self.quarzo.free_spots:
            self.quarzo.place(x, y)
            self.num_nodes_visited += 1

            if self.quarzo.check_winner() != -1:
                score = 1   #QuarzoAI's victory
            elif depth == 0:
                score = 0   #Depth constraint, dummy draw-score returned
            elif self.quarzo.check_finished():
                score = 0   #Draw
            else:
                score = self.max_piece(alpha=alpha, beta=beta, depth=depth)

            self.quarzo.unplace(x, y)

            best_score = max(best_score, score)
            alpha = max(alpha, best_score)
            if beta <= alpha:
                self.num_alpha_cut += 1
                break #pruning, alpha cutoff
        return best_score