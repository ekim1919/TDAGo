import os

import matplotlib.pyplot as plt
import matplotlib.animation as animate
from matplotlib.widgets import Slider
import numpy as np

from goripser import *
from persim import plot_diagrams


class PlotFSHandler: #Handles all parsing and file handling for plot printing

    def __init__(self,pathname):
        self.plot_root_dir = "/Users/edwardkim/Work/TDAGo/testplots/"

        dir_name = os.path.dirname(pathname)
        dir_name_index = dir_name.rfind('/')+1

        self.plot_dir = os.path.join(self.plot_root_dir,dir_name[dir_name_index:])
        self.file_name = os.path.split(pathname)[1]

        if(not os.path.isdir(self.plot_dir)):
            os.mkdir(self.plot_dir)

    def get_save_loc(self):
        return os.path.join(self.plot_dir,self.file_name)

class GameScroll:

    def __init__(self,pathname):
        self.pathname = pathname
        self.proc = SGFProcessor(pathname)
        self.figure = plt.figure(figsize=(10,10))

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

        self.wdist = self.figure.add_subplot(325)
        self.scroller = self.figure.add_subplot(326)

        self.x, self.y = (DistanceArray(self.pathname,0,400)).get_wass_array()
        self.l, = self.wdist.plot(self.x,self.y) #A lot of attributes. Should simplify this stuff sometime later if possible

        self.save_loc = PlotFSHandler(pathname).get_save_loc()

    def update(self,val):
        val = int(val)
        (black_stones, white_stones), (black_dgms,white_dgms) = self.get_move(val) #Someday figureout a caching solution to alleviate speed slowdown.

        self.white_board.clear()
        self.white_board.scatter(white_stones[:,0], white_stones[:,1], color='red') #anything more efficient then scattering it every time?
        self.black_board.clear()
        self.black_board.scatter(black_stones[:,0], black_stones[:,1],color='black')

        self.black_dgms = self.figure.add_subplot(324)
        plt.cla()
        self.black_dgms.set_title('Black PH') #Terribly way of just referencing the plot and clearing the plot to update Persistence Diagrams. Dnot feel like wrestlin with matplotlib right now.
        plot_diagrams(black_dgms)

        self.white_dgms = self.figure.add_subplot(322)
        plt.cla()
        self.white_dgms.set_title('White PH')
        plot_diagrams(white_dgms)

        self.l.set_data(self.x[:val],self.y[:val])

    def get_move(self,move_num): #Get dgms,board config for after single desired move
        return next(self.proc.filter_game(move_num,move_num+1))

    def scroll(self):

        spos = Slider(self.scroller,'Move #',1,self.proc.num_of_moves(),valstep=1)
        spos.on_changed(self.update)
        plt.show()

class GameAnimator: #animates the persistence diagrams and board to see how game progresses

    def __init__(self,pathname):
        self.pathname = pathname
        self.proc = SGFProcessor(pathname)
        self.figure = plt.figure(figsize=(10,10))

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

        self.wdist = self.figure.add_subplot(325)

        self.save_loc = PlotFSHandler(pathname).get_save_loc()
        self.draw_board(self.black_board)
        self.draw_board(self.white_board)


    def draw_board(self,ax):

        for i in range(19):
            ax.axhline(i,color="black")
            ax.axvline(i,color="black")
        ax.set_facecolor('burlywood')

    def update(self,data_tup,x,y,l):
        (black_stones, white_stones), (black_dgms,white_dgms) = data_tup[0]
        num = data_tup[1]

        self.white_board.scatter(white_stones[:,0], white_stones[:,1], color='red',s=250) #anything more efficient then scattering it every time?
        self.black_board.scatter(black_stones[:,0], black_stones[:,1],color='black',s=250)

        plt.sca(self.black_dgms)
        plt.cla()
        self.black_dgms.set_title('Black PH') #Terribly way of just referencing the plot and clearing the plot to update Persistence Diagrams. Dnot feel like wrestlin with matplotlib right now.
        plot_diagrams(black_dgms)

        plt.sca(self.white_dgms)
        plt.cla()
        self.white_dgms.set_title('White PH')
        plot_diagrams(white_dgms)

        l.set_data(x[:num],y[:num])
        return l,

    def animate(self):
        x,y = (DistanceArray(self.pathname,0,400)).get_wass_array()
        l, = self.wdist.plot(x,y)
        ani = animate.FuncAnimation(self.figure,self.update,frames=zip(self.proc.filter_game(0,400),range(400)), fargs=[x,y,l],save_count=400)

        Writer = animate.writers['ffmpeg']
        writer = Writer(fps=10,bitrate=-1)
        ani.save(self.save_loc + ".mp4",writer=writer) #save animation

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

        ax.set(xlabel="Move #",ylabel="Avg Conn between groups",title="Plot Of Avg Conn as " + self.name + " progresses. (Winner:" + proc.winner + ")" )
        plt.savefig(self.save_loc + "_conngraph.png")

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
