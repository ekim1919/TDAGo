from sgfmill import sgf
from sgfmill import sgf_moves

from ripser import ripser
from persim import plot_diagrams
from persim import wasserstein, wasserstein_matching
from persim import bottleneck, bottleneck_matching

import numpy as np
import matplotlib.pyplot as plt
import scipy.spatial.distance as dist

class SGFProcessor: #Takes SGF files and converts to TDA-ready data. Might be worth revamping this into becoming an iterator

    def __init__(self,pathname):
        self.pathname = pathname

        with open(self.pathname, "rb") as f:
            sgf_src = f.read()

        try:
            sgf_game = sgf.Sgf_game.from_bytes(sgf_src)
        except:
            raise Exception("SGF file format error")
        try:
            _ , self.play_seq = sgf_moves.get_setup_and_moves(sgf_game)
        except:
            raise Exception(str(e))

    #Gives total number of moves in a game.
    def num_of_moves(self):
        return len(self.play_seq)

    def filter_game(self, start_num, finish_num, stone_color=None):

            plays = self.play_seq[:finish_num] #Slice play list by desired move number

            black_move_pos = np.empty([0,2])
            white_move_pos = np.empty([0,2])

            move_list = zip(plays, range(finish_num)) #Iteretor for sequence of moves and their indices

            for (color, move), num in move_list:
                row, col = move
                if (color == 'b'):
                    black_move_pos = np.append(black_move_pos,[[row,col]],axis=0)
                else:
                    white_move_pos = np.append(white_move_pos,[[row,col]],axis=0)

                black_dgms = TDATools.filter_rips(black_move_pos)
                white_dgms = TDATools.filter_rips(white_move_pos)

                if num >= start_num: #Don't start iterating until we get to move of interest.
                    yield (black_move_pos, white_move_pos), (black_dgms, white_dgms) #Given in double tuple format with board and dgms positions in that order


class TDATools: #Revise this later.

    #returns relevant dgms for matrix of stone positions
    @staticmethod
    def filter_rips(move_pos):
        pdis = dist.squareform(dist.pdist(move_pos,'cityblock'))
        return ripser(pdis,distance_matrix=True)['dgms']

    @staticmethod
    def match_wasserstein(dgms1, dgms2):
        return wasserstein(dgms1[1],dgms2[1],matching=True)

    @staticmethod
    def match_bottleneck(dgms1,dgms2):
        return bottleneck(dgms1[1],dgms2[1], matching=True)
