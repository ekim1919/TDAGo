from sgfmill import sgf
from sgfmill import sgf_moves

from ripser import ripser
from persim import plot_diagrams
from persim import wasserstein, wasserstein_matching

import numpy as np
import matplotlib.pyplot as plt
import scipy.spatial.distance as dist

import sys

class SGFProcessor: #Takes SGF files and converts to TDA-ready data

    def __init__(self,pathname):
        self.pathname = pathname

    def process_sgf_file(self, move_number, stone_color=None):

            with open(self.pathname, "rb") as f:
                sgf_src = f.read()

            try:
                sgf_game = sgf.Sgf_game.from_bytes(sgf_src)
            except:
                raise Exception("sgf file format error")

            try:
                _ , plays = sgf_moves.get_setup_and_moves(sgf_game)
            except:
                raise Exception(str(e))

            move_number = max(0, move_number-1)
            plays = plays[:move_number]

            move_pos = np.zeros((move_number,2))
            iter_arr = list(zip(plays,move_pos))

            black_move_pos = []
            white_move_pos = []

            for (color, move), a in iter_arr: #Create positions of stones
                if color == 'b':
                    black_move_pos.append(move[0])
                    black_move_pos.append(move[1])
                else:
                    white_move_pos.append(move[0])
                    white_move_pos.append(move[1])

            black_move_pos = np.asarray(black_move_pos).reshape(-1,2)
            white_move_pos = np.asarray(white_move_pos).reshape(-1,2)

            black_dgms = TDATools.filter_rips(black_move_pos)
            white_dgms = TDATools.filter_rips(white_move_pos)

            return black_move_pos, white_move_pos, black_dgms, white_dgms


class TDATools: #REvise this later.

    #returns relevant dgms for matrix of stone positions
    @staticmethod
    def filter_rips(move_pos):
        pdis = dist.squareform(dist.pdist(move_pos,'cityblock'))
        return ripser(pdis,distance_matrix=True)['dgms']

    @staticmethod
    def match_wasserstein(dgms1, dgms2):
        return wasserstein(dgms1[1],dgms2[1],matching=True)

class Plotter:

    def __init__(self, processor):
        self.processor = processor


    def plot_move(self, move_num):

            plt.figure(figsize=(150,30))

            black_stones, white_stones, black_dgms, white_dgms = (self.processor).process_sgf_file(move_num)

            plt.subplot(331)
            plt.xticks(np.arange(20))
            plt.scatter(white_stones[:,0], white_stones[:,1], color='red')
            plt.title('White Stone Positions')

            plt.subplot(332)
            plt.title('White PH')
            plot_diagrams(white_dgms)

            plt.subplot(336)
            plt.scatter(black_stones[:,0], black_stones[:,1],color='black')
            plt.scatter(white_stones[:,0], white_stones[:,1], color='red')
            plt.title('Total Board')

            plt.subplot(337)
            plt.xticks(np.arange(20))
            plt.scatter(black_stones[:,0], black_stones[:,1], color='black')
            plt.title('Black Stone Positions')

            plt.subplot(338)
            plt.title('Black PH')
            plot_diagrams(black_dgms)

            plt.show()

    #Plots wasserstein matching between two consec moves for both colors
    def plot_wass_match(self, move_num):

        plt.figure(figsize=(150,30))

        _,_, bdgms1, wdgms1 = (self.processor).process_sgf_file(move_num)
        #_,_, bdgms2, wdgms2 = (self.processor).process_sgf_file(move_num+20)

        wdist, (match,_) = TDATools.match_wasserstein(wdgms1,bdgms1)

        plt.subplot(122)
        wasserstein_matching(wdgms1[1], bdgms1[1], match)
        plt.title("Matching for Move %i"%move_num)
        print(wdist)

        plt.show()


def main(argv):
    plotter = Plotter(SGFProcessor(argv[0]))
    plotter.plot_wass_match(int(argv[1]))


if __name__ == '__main__':
    main(sys.argv[1:])
