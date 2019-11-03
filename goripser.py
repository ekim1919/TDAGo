from sgfmill import sgf
from sgfmill import sgf_moves

from ripser import ripser
from persim import plot_diagrams

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

            print(black_move_pos)

            return black_move_pos, white_move_pos

        black_pdis = dist.squareform(dist.pdist(black_move_pos,'cityblock'))
        black_dgms = ripser(black_pdis,distance_matrix=True)['dgms']

#returns relevant dgms for matrix of stone positions
def ripsfiltrator(move_pos):
        pdis = dist.squareform(dist.pdist(move_pos,'cityblock'))
        return ripser(pdis,distance_matrix=True)['dgms']


def plot_move(move_number, processor):

        plt.figure(figsize=(150,30))

        black_move_pos, white_move_pos = processor.process_sgf_file(move_number)

        plt.subplot(331)
        plt.xticks(np.arange(20))
        plt.scatter(white_move_pos[:,0], white_move_pos[:,1], color='red')
        plt.title('White Stone Positions')

        white_dgms = ripsfiltrator(white_move_pos)

        plt.subplot(332)
        plt.title('White PH')
        plot_diagrams(white_dgms)

        #plt.subplot(336)
        #total_board
        #plt.scatter(total_board[:,0], total_board[:,1])
        #plt.title('Total Board')

        plt.subplot(337)
        plt.xticks(np.arange(20))
        plt.scatter(black_move_pos[:,0], black_move_pos[:,1], color='black')
        plt.title('Black Stone Positions')

        black_dgms = ripsfiltrator(black_move_pos)

        plt.subplot(338)
        plt.title('Black PH')
        plot_diagrams(black_dgms)

        plt.show()

def main(argv):
    plot_move(int(argv[1]), SGFProcessor(argv[0]))


if __name__ == '__main__':
    main(sys.argv[1:])
