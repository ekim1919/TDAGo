import os

import matplotlib.pyplot as plt
import matplotlib.animation as animate
from matplotlib.widgets import Slider, TextBox
import numpy as np

from routines import *

from multiprocessing import Pool
from copy import copy

class PlotFSHandler: #Handles all parsing and file handling for plot printing

    def __init__(self,pathname):

        self.plot_root_dir = os.path.join(os.environ['HOME'], "/Work/TDAGo/testplots/")

        dir_name = os.path.dirname(pathname)
        dir_name_index = dir_name.rfind('/')+1

        self.plot_dir = os.path.join(self.plot_root_dir,dir_name[dir_name_index:])
        self.file_name = os.path.split(pathname)[1]

        if(not os.path.isdir(self.plot_dir)):
            os.mkdir(self.plot_dir)

    def get_save_loc(self):
        return os.path.join(self.plot_dir,self.file_name)



class GameAnimator: #animates the persistence diagrams and board to see how game progresses

    def __init__(self,pathname):
        self.pathname = pathname
        self.figure = plt.figure(figsize=(25,25))
        self.proc = SGFProcessor(pathname)

        self.board_rout = BoardPHAniRoutine(self.figure,[(321,322),(323,324)],self.proc) #Testing these routines for now. Animator will have to be more abstracted later
        self.wdist = WassAniRoutine(self.figure,325,self.pathname)

        self.move_box = MoveBoxRoutine(self.figure,326)
        self.save_loc = PlotFSHandler(pathname).get_save_loc()

    def init(self):
        self.line = self.wdist.init_routine()

    def update(self,i,line):
        self.board_rout.update(i)
        self.move_box.update(i)
        return self.wdist.update(i)

    def animate(self):
        num_moves = self.proc.num_of_moves()
        self.init()
        ani = animate.FuncAnimation(self.figure,self.update,frames=num_moves,fargs=[self.line], save_count=400)

        Writer = animate.writers['ffmpeg']
        writer = Writer(fps=10,bitrate=-1)
        ani.save(self.save_loc + ".mp4",writer=writer) #save animation


class StaticPlot: #Simply outputs one routine as a png plot

    def __init__(self,pathname,routine,start=0,finish=400):
        #assert
        self.save_loc = PlotFSHandler(pathname).get_save_loc()
        self.figure = plt.Figure((20,20))
        name = os.path.split(pathname)[1]
        self.routine = routine(self.figure,111,pathname,start=start,finish=finish,name=name)

    def plot(self): #We simply run the plotting routines and save them to disk

        self.routine.run()
        self.figure.savefig(self.save_loc + ".png") #Save file in corresponding directory


class SaveGameProg: #animates the persistence diagrams and board to see how game progresses

    def __init__(self,pathname):
        self.pathname = pathname
        self.proc = SGFProcessor(pathname)
        self.figure = plt.figure(figsize=(20,20))

        self.white_board = self.figure.add_subplot(321)
        self.white_board.set_xticks(np.arange(20))
        self.white_board.set_yticks(np.arange(20))
        self.white_board.set_title('White Stone Positions')

        self.white_dgms = self.figure.add_subplot(322)
        self.white_dgms.set_title('White PH')

        self.black_board = self.figure.add_subplot(323) #Make plots wider for better visibility
        self.black_board.set_xticks(np.arange(20))
        self.black_board.set_yticks(np.arange(20))
        self.black_board.set_title('Black Stone Positions')

        self.black_dgms = self.figure.add_subplot(324)
        self.black_dgms.set_title('Black PH')

        self.save_loc = PlotFSHandler(pathname).get_save_loc()
        self.draw_board(self.black_board)
        self.draw_board(self.white_board)

    def draw_board(self,ax):

        for i in range(19):
            ax.axhline(i,color="black")
            ax.axvline(i,color="black")
        ax.set_facecolor('burlywood')

    def update(self,data_tup):
        (black_stones, white_stones), (black_dgms,white_dgms) = data_tup

        self.white_board.scatter(white_stones[:,0], white_stones[:,1], color='red',s=150) #anything more efficient then scattering it every time?
        self.black_board.scatter(black_stones[:,0], black_stones[:,1],color='black',s=150)

        plt.sca(self.black_dgms)
        plt.cla()
        self.black_dgms.set_title('Black PH') #Terribly way of just referencing the plot and clearing the plot to update Persistence Diagrams. Dnot feel like wrestlin with matplotlib right now.
        plot_diagrams(black_dgms)

        plt.sca(self.white_dgms)
        plt.cla()
        self.white_dgms.set_title('White PH')
        plot_diagrams(white_dgms)

    def plot(self):

        if(not os.path.isdir(self.save_loc)):
            os.mkdir(self.save_loc)

        #pool = Pool(processes=6)
        for data_tup, num in zip(self.proc.filter_game(0,400),range(400)):
            self.update(data_tup)
            self.figure.savefig(os.path.join(self.save_loc,str(num) + ".png"))
            #pool.apply(fig.savefig, args=(os.path.join(self.save_loc,str(num) + ".png"),))
        #pool.close()
        #pool.join()

class Analytics: #Simply outputs evolution of distance as a plot.

    def __init__(self,pathname,start=0,finish=400):
        self.disarr = DistanceArray(pathname,start,finish)
        self.pathname = pathname
        self.save_loc = PlotFSHandler(pathname).get_save_loc()
        self.name = os.path.split(pathname)[1]
        self.start_num = start
        self.finish_num = finish

    def game_avg_conn(self):
        proc = SGFProcessor(self.pathname)
        black_conn = []
        white_conn = []

        for _, dgms in proc.filter_game(0,400):
            black_h1, white_h1 = dgms[0][1], dgms[1][1]
            black_mean, white_mean = np.mean(black_h1,axis=0), np.mean(white_h1,axis=0)
            black_conn.append(black_mean[0])
            white_conn.append(white_mean[0])
        x = np.arange(proc.num_of_moves())

        fig, ax = plt.subplots()
        ax.plot(x,black_conn,color="black",label=proc.black_player)
        ax.plot(x,white_conn,color="red",label=proc.white_player)
        ax.legend()

        ax.set(xlabel="Move #",ylabel="Avg Distance of detected groups",title="Plot Of Avg Distance  as " + self.name + " progresses. (Winner:" + proc.winner_name + ")" )
        plt.savefig(self.save_loc + "_conngraph.png")

    def game_scoring(self):

        def score(h1_dgms):
            acc = 0
            for i in h1_dgms:
                d = i[1]
                b = i[0]
                # acc +=
            return acc

        proc = SGFProcessor(self.pathname)
        black_score = []
        white_score = []
        x = np.arange(proc.num_of_moves())

        for _, dgms in proc.filter_game(0,400):
            black_h1, white_h1 = dgms[0][1], dgms[1][1]
            black_score.append(score(black_h1))
            white_score.append(score(white_h1))

        fig, ax = plt.subplots()
        ax.plot(x,black_score,color="black",label=proc.black_player)
        ax.plot(x,white_score,color="red",label=proc.white_player)
        ax.legend()

        ax.set(xlabel="Move #",ylabel="Score",title="Plot Of Score as " + self.name + " progresses. (Winner:" + proc.winner + ")" )
        plt.savefig(self.save_loc + "_scoregraph.png")

    def game_wdist(self):

        x,y = self.disarr.get_wass_array()

        fig,ax = plt.subplots()
        ax.plot(x,y,1)
        ax.set(xlabel='Move #',ylabel='Wasserstein Dist',title="Plot Of WDist as " + self.name + " progresses")
        plt.savefig(self.save_loc + "_wdist.png") #Save file in corresponding directory

    def  game_bdist(self):

        x,y = self.disarr.get_bottle_array()

        ax.plot(x,y,1)
        ax.set(xlabel='Move #',ylabel='Bottleneck Dist',title="Plot Of BDist as " + self.name + " progresses")
        plt.savefig(self.save_loc + ".png") #Save file in corresponding directory
