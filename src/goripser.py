from sgfmill import sgf
from sgfmill import sgf_moves

from ripser import ripser
from persim import plot_diagrams
from persim import wasserstein, wasserstein_matching

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
            raise Exception("sgf file format error")

        try:
            _ , self.play_seq = sgf_moves.get_setup_and_moves(sgf_game)
        except:
            raise Exception(str(e))

    def filter_game(self, move_num=None, stone_color=None):

            #assert not move_num < 0 #Move number should    if move_num is not None: #Slice to desired move number if required. not be negative

            plays = self.play_seq[:move_num] #Slice play list by desired move number

            black_move_pos = np.empty([0,2])
            white_move_pos = np.empty([0,2])

            for (color, move) in plays:
                row, col = move
                if (color == 'b'):
                    black_move_pos = np.append(black_move_pos,[[row,col]],axis=0)
                else:
                    white_move_pos = np.append(white_move_pos,[[row,col]],axis=0)

                black_dgms = TDATools.filter_rips(black_move_pos)
                white_dgms = TDATools.filter_rips(white_move_pos)

                yield (black_move_pos, white_move_pos), (black_dgms, white_dgms)


    #Gives total number of moves in a game.
    def num_of_moves(self):
        return len(self.play_seq)


class Analytics: #Will work for now. Generalize this to put analysis plots into specific directories

    def __init__(self,pathname):
        self.proc = SGFProcessor(pathname)
        self.plotdir = "/playpen/ehkim/work/TDAGo/testplots/"
        self.name = pathname[pathname.rfind('/'):]

    def game_wdist(self):

        val = []
        for _, dgms in (self.proc).filter_game():
            wdist, _ = TDATools.match_wasserstein(dgms[0],dgms[1])
            val.append(wdist)

        fig,ax = plt.subplots()
        ax.plot(np.arange(1,(self.proc).num_of_moves()+1,1),val)

        plt.savefig(self.plotdir + self.name + ".png")

class TDATools: #Revise this later.

    #returns relevant dgms for matrix of stone positions
    @staticmethod
    def filter_rips(move_pos):
        pdis = dist.squareform(dist.pdist(move_pos,'cityblock'))
        return ripser(pdis,distance_matrix=True)['dgms']

    @staticmethod
    def match_wasserstein(dgms1, dgms2):
        return wasserstein(dgms1[1],dgms2[1],matching=True)
