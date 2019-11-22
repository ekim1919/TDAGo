from abc import ABC, abstractmethod

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animate
from matplotlib.widgets import Slider, TextBox

from goripser import *
from persim import plot_diagrams

class Routine():

    def __init__(self,figure, plot_cood, title=None):
        self.figure = figure
        self.ax = self.figure.add_subplot(plot_cood)
        self.title = title

        if self.title is not None:
            self.ax.set_title(self.title)

class StaticRoutine(Routine,ABC):

    @abstractmethod
    def run(self):
        pass

class AniRoutine(Routine,ABC):

    @abstractmethod
    def init_routine(self):
        pass

    @abstractmethod
    def update(self,index):
        pass


#Routine responsible for calculating and plotting WDist of a game
class WassRoutine(StaticRoutine):

    def __init__(self, figure, plot_cood, pathname,start=0,finish=400,name='game'):

        assert isinstance(figure,plt.Figure) #Gotta work with figures here.
        super().__init__(figure,plot_cood)

        self.x, self.y = (DistanceArray(pathname,start,finish)).get_wass_array() #Get the wass array for game at pathname
        self.name = name

    def run(self):

       self.ax.plot(self.x,self.y,1)
       self.ax.set(xlabel='Move #',ylabel='Wasserstein Dist',title="Plot Of WDist as " + self.name + " progresses")


class BottleRoutine(StaticRoutine):

    def __init__(self, figure, plot_cood, pathname,start=0,finish=400,name='game'):

        assert isinstance(figure,plt.Figure) #Gotta work with figures here.
        super().__init__(figure,plot_cood)

        self.x, self.y = (DistanceArray(pathname,start,finish)).get_bottle_array() #Get the wass array for game at pathname
        self.name = name

    def run(self):

       self.ax.plot(self.x,self.y,1)
       self.ax.set(xlabel='Move #',ylabel='Wasserstein Dist',title="Plot Of BDist as " + self.name + " progresses")

class WassAniRoutine(AniRoutine):

    def __init__(self,figure,plot_cood,pathname,start=0,finish=400):
        super().__init__(figure, plot_cood,title="WDist Progression")

        self.ax.set_xlabel("Move #")
        self.ax.set_ylabel("WDist between White and Black")

        self.x, self.y = (DistanceArray(pathname,start,finish)).get_wass_array() #Get the wass array for game at pathname

    def init_routine(self):
        self.ax, = self.ax.plot(self.x[:1],self.y[:1])
        return self.ax

    def update(self,index):
        self.ax.set_data(self.x[:index],self.y[:index])
        return self.ax

class DGMSAniRoutine(AniRoutine):

    def __init__(self,figure,plot_cood,color):
        self.color = "White" if color == 'w' else "Black"
        super().__init__(figure, plot_cood,title= self.color + " PH")

    def init_routine(self): #Don't have to init anything for PH
        pass

    def update(self,dgms):
        plt.sca(self.ax) #change active subplot to relevant one
        plt.cla() #figure out how to use gca for this
        self.ax.set_title(self.title)
        plot_diagrams(dgms)

class BoardDrawRoutine(AniRoutine): #Only supports single color for now.

    def __init__(self,figure,plot_cood,color):
        super().__init__(figure, plot_cood,title= color + " Stone Positions")
        self.ax.set_xticks(np.arange(20))
        self.ax.set_yticks(np.arange(20))
        self.__draw_board(self.ax)
        self.color = 'red' if color == 'w' else 'black' #using red color scheme for white stones for constrast on board

    def __draw_board(self,ax):
        for i in range(19):
            ax.axhline(i,color="black")
            ax.axvline(i,color="black")
        ax.set_facecolor('burlywood')

    def init_routine(self):
        pass

    def update(self,board_pos):
        self.ax.scatter(board_pos[:,0], board_pos[:,1], color=self.color,s=250)

class BoardPHAniRoutine(AniRoutine):

    def __init__(self,figure,plot_cood_tups,proc): #(black,white)
        assert isinstance(proc,SGFProcessor)

        self.rout_list =  [BoardDrawRoutine(figure,plot_cood_tups[0][0],'b'), DGMSAniRoutine(figure,plot_cood_tups[0][1],'b'),
                           BoardDrawRoutine(figure,plot_cood_tups[1][0],'w'), DGMSAniRoutine(figure,plot_cood_tups[1][1],'w')]
        self.proc = proc
        self.board_list = [i for i in (self.proc).filter_game(0,400)] #Comsumes a lot of memory. I'm going to have to revuse filter_game to ensure modularity here

    def init_routine(self):
        pass

    def update(self,index):
        board, dgms = self.board_list[index]
        self.rout_list[0].update(board[0])
        self.rout_list[1].update(dgms[0])
        self.rout_list[2].update(board[1])
        self.rout_list[3].update(dgms[1])

class MoveBoxRoutine(AniRoutine):

    def __init__(self,figure,plot_cood):
        super().__init__(figure,plot_cood)
        self.move_box = TextBox(self.ax,'Move #: ',0)

    def init_routine(self):
        pass

    def update(self,index):
        self.move_box.set_val(index)


class WassMatchAniRoutine(AniRoutine):

    def __init__(self,figure,plot_cood):
        super().__init__(figure,plot_cood)

    def init_routine(self):
        pass

    
