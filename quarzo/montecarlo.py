import random
from .quarzo import Quarzo

class MonteCarlo():
    def __init__(self, quarzo: Quarzo):
        self.quarzo = quarzo
        self.num_matches = 20 #number of matches to simulate per child node
    
    def choose_piece(self) -> int:
        '''
        Runs a simulation for every possible choice of piece to give
        the opponent. Returns the piece that yields the highest win ratio.
        '''
        choice_reward_dict = {} #keys: choice, values: ratio of won games
        pieces = self.quarzo.usable_pieces
        random.shuffle(pieces)
        for p in pieces:
            choice_reward_dict[p] = 0.0
    
        for p in pieces: 
            score = 0.0

            for _ in range(self.num_matches):
                #Runs the first ply with the selected piece
                self.quarzo.select(p)
                self.quarzo.switch_player()
                (x, y) = random.choice(self.quarzo.free_spots)
                self.quarzo.place(x, y)

                #Starts the simulation
                score += self.__run_simulation()
                self.quarzo.reset_board_status()

            win_ratio = score / self.num_matches
            choice_reward_dict[p] = win_ratio

        piece = max(choice_reward_dict.keys(), key=(lambda k: choice_reward_dict[k]))
        return piece

    def place_piece(self) -> tuple[int, int]:
        '''
        Runs a simulation for every possible choice of a spot to place the piece in. 
        Returns the coordinates of the spot that yields the highest win ratio.
        '''
        choice_reward_dict = {} #keys: choice, values: ratio of won games
        moves = self.quarzo.free_spots
        random.shuffle(moves)
        for (x, y) in moves:
            choice_reward_dict[(x, y)] = 0.0
    
        for (x, y) in moves:
            score = 0.0

            for _ in range(self.num_matches):
                #Finishes the first ply with the selected move
                self.quarzo.place(x, y)

                #Starts the simulation
                score += self.__run_simulation()
                self.quarzo.reset_board_status()

            win_ratio = score / self.num_matches
            choice_reward_dict[(x, y)] = win_ratio

        place = max(choice_reward_dict.keys(), key=(lambda k: choice_reward_dict[k]))
        # print('Reward dict:')
        # for k in choice_reward_dict.keys():
        #     print(f'{k}: {choice_reward_dict[k]:.2f}')
        # print(f'Choice: {place}')
        return place
    
    def __run_simulation(self) -> float:
        '''
        Runs a random game until the end.
        Returns 1 for victory, 0.5 for draw, 0 for defeat.
        '''
        transform_result = {0: 0.0, -1: 0.5, 1: 1.0} #defeat, draw, victory
        self.quarzo.current_player = 1

        winner = -1
        while winner < 0 and not self.quarzo.check_finished():
            self.quarzo.select(random.choice(self.quarzo.usable_pieces))
            (x, y) = random.choice(self.quarzo.free_spots)
            self.quarzo.place(x, y)
            winner = self.quarzo.check_winner()
        return transform_result[winner]
