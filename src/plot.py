import os
import matplotlib.pyplot as plt
import matplotlib.animation as animate
from goripser import SGFProcessor

class PlotFSHandler: #Handles all parsing and file handling for plot printing

    def __init__(self,pathname):
        self.plot_root_dir = "/playpen/ehkim/work/TDAGo/testplots/"

        dir_name = os.path.dirname(pathname)
        dir_name_index = dir_name.rfind('/')+1

        self.plot_dir = os.path.join(self.plot_root_dir,dir_name[dir_name_index:])

        self.file_name = os.path.split(pathname)[1]

        if(not os.path.isdir(self.plot_dir)):
            os.mkdir(self.plot_dir)

    def get_save_loc(self):
        return os.path.join(self.plot_dir,self.file_name)

class GameAnimator:

    def __init__(self,pathname):
        self.proc = SGFProcessor(pathname)
        self.figure = plt.figure()

        self.white_board = self.figure.add_subplot(331)
        self.white_board.set_xticks(np.arange(20))
        self.white_board.set_title('White Stone Positions')

        self.white_dgms = self.figure.add_subplot(332)
        self.white_dgms.set_title('White PH')

        self.total_board = self.figure.add_subplot(336)
        self.total_board.set_title('Total Board')


        self.black_board = self.figure.add_subplot(337) #Make plots wider for better visibility
        self.black_board.set_xticks(np.arange(20))
        self.black_board.set_title('Black Stone Positions')

        self.black_dgms = self.figure.add_subplot(338)
        self.black_dgms.set_title('Black PH')

        self.save_loc = PlotFSHandler(pathname).get_save_loc()

    def update(self,data_tup):
        (black_stones, white_stones), (black_dgms,white_dgms) = data_tup

        self.white_board.scatter(white_stones[:,0], white_stones[:,1], color='red') #anything more efficient then scattering it every time?
        self.black_board.scatter(black_stones[:,0], black_stones[:,1],color='black')


    def animate(self):
        ani = animate.FuncAnimation(self.figure,self.update,frames=self.proc.filter_game(0,400))
        Writer = animate.writers['ffmpeg']
        writer = Writer(fps=10)
        ani.save(self.save_loc + ".mp4",writer=writer) #save animation

class Analytics: #Put into different file

    def __init__(self,pathname,start=0,finish=400):
        self.proc = SGFProcessor(pathname)
        self.save_loc = PlotFSHandler(pathname).get_save_loc()
        self.start_num = start
        self.finish_num = finish

    def game_wdist(self):

        val = []
        for _, dgms in (self.proc).filter_game(start_num=self.start_num,finish_num=self.finish_num):
            wdist, _ = TDATools.match_wasserstein(dgms[0],dgms[1])
            val.append(wdist)

        fig,ax = plt.subplots()
        ax.plot(np.arange(self.start_num,
                         ((self.proc).num_of_moves() if self.finish_num == 400 else (self.finish_num) + 1), 1) #probably should create generic class to handle actual plotting
                         ,val)
        ax.set(xlabel='Move #',ylabel='Wasserstein Dist',title="Plot Of WDist as " + self.name + " progresses")
        plt.savefig(self.save_loc + ".png") #Save file in corresponding directory

    def  game_bdist(self):

        val = []
        for _, dgms in (self.proc).filter_game(start_num=self.start_num,finish_num=self.finish_num):
            bdist, _ = TDATools.match_bottleneck(dgms[0],dgms[1])
            val.append(bdist)

        fig,ax = plt.subplots()
        ax.plot(np.arange(self.start_num,
                ((self.proc).num_of_moves() if self.finish_num == 400 else (self.finish_num) + 1)
                ,1),val)

        ax.set(xlabel='Move #',ylabel='Bottleneck Dist',title="Plot Of BDist as " + self.name + " progresses")
        plt.savefig(self.save_loc + ".png") #Save file in corresponding directory
