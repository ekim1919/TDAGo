from sgfmill import sgf
from sgfmill import sgf_moves

from ripser import ripser
from persim import wasserstein, wasserstein_matching
from persim import bottleneck, bottleneck_matching

import numpy as np
import scipy.spatial.distance as dist
from multiprocessing import Process, Queue, Array, Pool
from copy import copy

color_num = {'b':0, 'w':1}

class SGFProcessor:

    def __init__(self,pathname):
        self.pathname = pathname

        num_of_threads = 100

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

        self.black_move_pos = []
        self.white_move_pos = []

        self.dgms_arr = [[-1,-1] for _ in range(self.num_of_moves())]

        black_moves = np.empty([0,2]) #accumlator variables
        white_moves = np.empty([0,2])

        pool = Pool(6)

        for (color, move), num in zip(self.play_seq, range(self.num_of_moves())):
                row, col = move
                if (color == 'b'):
                    black_moves = np.append(black_moves,[[row,col]],axis=0)
                    pool.map(self.cal_dgms, [(num,'b', copy(black_moves))])
                else:
                    white_moves = np.append(white_moves,[[row,col]],axis=0)
                    pool.map(self.cal_dgms, [(num,'w', copy(white_moves))])

                self.black_move_pos.append(copy(black_moves)) #Using a lot of memory for the sake of convienence.
                self.white_move_pos.append(copy(white_moves))

        pool.close()
        pool.join()

    def cal_dgms(self, board_tup):
        index, color, board = board_tup
        color_index = color_num[color]
        self.dgms_arr[index][color_index] = TDATools.filter_rips(board)

    def num_of_moves(self): #Gives total number of moves in a game.
        return len(self.play_seq)

    def filter_game(self, start, finish, stone_color=None):

            finish = min(finish, self.num_of_moves())
            for i in range(start, finish):

                print(self.dgms_arr)

                black_index = i - 1 if self.dgms_arr[i][0] == -1 else i
                black_dgms = self.dgms_arr[black_index][0]

                white_index = i - 1 if self.dgms_arr[i][1] == -1 else i
                white_dgms = self.dgms_arr[white_index][1]

                yield (self.black_move_pos[i], self.white_move_pos[i]), (black_dgms, white_dgms) #Given in double tuple format with board and dgms positions in that order

class DistanceArray:

    def __init__(self,pathname,start,finish):
        self.start = start
        self.finish = finish
        self.proc = SGFProcessor(pathname)

    def get_wass_array(self): #bottlenecked by filtration
        y = []
        for _, dgms in (self.proc).filter_game(self.start,self.finish):
            wdist, _ = TDATools.match_wasserstein(dgms[0],dgms[1])
            y.append(wdist)

        x = np.arange(self.start,
                      min(self.proc.num_of_moves(),self.finish))
        return x,y

    def get_bottle_array(self):
        y = []
        for _, dgms in (self.proc).filter_game(self.start,self.finish):
            wdist, _ = TDATools.match_bottleneck(dgms[0],dgms[1])
            y.append(wdist)
        x = np.arange(self.start,
                      min(self.proc.num_of_moves(),self.finish))
        return x,y

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
