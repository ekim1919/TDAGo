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

        black_moves = np.empty([0,2]) #accumlator variables
        white_moves = np.empty([0,2])

        pool = Pool(processes=6)
        process_results = [] #list of processes

        for (color, move), num in zip(self.play_seq, range(self.num_of_moves())):
                row, col = move
                if (color == 'b'):
                    black_moves = np.append(black_moves,[[row,col]],axis=0)
                    process_results.append(pool.apply_async(self.cal_dgms,args=((num,color,black_moves),)))
                else:
                    white_moves = np.append(white_moves,[[row,col]],axis=0)
                    process_results.append(pool.apply_async(self.cal_dgms,args=((num,color,white_moves),)))

                self.black_move_pos.append(copy(black_moves)) #Using a lot of memory for the sake of convienence.
                self.white_move_pos.append(copy(white_moves))
        pool.close()
        pool.join()

        self.dgms_list = [p.get() for p in process_results]
        self.dgms_list.sort()
        self.empty_dgms = TDATools.filter_rips(np.empty([0,2]))

    def cal_dgms(self, board_tup):
        index, color, board = board_tup
        return (index, color, TDATools.filter_rips(board))

    def num_of_moves(self): #Gives total number of moves in a game.
        return len(self.play_seq)

    def filter_game(self, start, finish):

            finish = min(finish, self.num_of_moves())
            for i in range(start, finish):
                j = max(0, i-1)
                yield (self.black_move_pos[i], self.white_move_pos[i]), (self.dgms_list[i][2], self.dgms_list[j][2] if j > 0 else self.empty_dgms)

class DistanceArray:

    def __init__(self,pathname,start,finish): #Account for new arch
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
