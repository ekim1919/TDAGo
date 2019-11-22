import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animate
from matplotlib.widgets import Slider, TextBox

from goripser import *
from persim import plot_diagrams

class Routine():

    def __init__(self,figure, plot_cood):
        self.figure = figure
        self.ax = self.figure.add_subplot(plot_cood)

    def run(self):
        pass

    def update(self):
        pass


#Routine responsible for calculating and plotting WDist of a game
class WassRoutine(Routine):

    def __init__(self, figure, plot_cood, pathname,start=0,finish=400,name='game'):

        assert isinstance(figure,plt.Figure) #Gotta work with figures here.
        super().__init__(figure,plot_cood)

        self.x, self.y = (DistanceArray(pathname,start,finish)).get_wass_array() #Get the wass array for game at pathname
        self.name = name

    def run(self):

       self.ax.plot(self.x,self.y,1)
       self.ax.set(xlabel='Move #',ylabel='Wasserstein Dist',title="Plot Of WDist as " + self.name + " progresses")

class BottleRoutine(Routine):

    def __init__(self, figure, plot_cood, pathname,start=0,finish=400,name='game'):

        assert isinstance(figure,plt.Figure) #Gotta work with figures here.
        super().__init__(figure,plot_cood)

        self.x, self.y = (DistanceArray(pathname,start,finish)).get_bottle_array() #Get the wass array for game at pathname
        self.name = name

    def run(self):

       self.ax.plot(self.x,self.y,1)
       self.ax.set(xlabel='Move #',ylabel='Wasserstein Dist',title="Plot Of BDist as " + self.name + " progresses")

class DGMSRoutine(Routine):
    
