from plot import *

import sys
import os
import warnings
warnings.filterwarnings("ignore") #Ignore warnings for now

from experiments import *

def main(argv):

    #run_conn_routine(str(argv[0]))
    predict_avg_experi(str(argv[0]))
    
def run_wass_routine(dir):

    sgf_files = []
    for files in os.listdir(dir):
        if files.endswith(".sgf"):
            sgf_files.append(os.path.join(dir,files)) #probably should create a routunes class to abstract his iteration stuff out

    for game_file_paths in sgf_files:
        Analytics(game_file_paths).game_wdist()

def run_conn_routine(dir):

    sgf_files = []
    for files in os.listdir(dir):
        if files.endswith(".sgf"):
            sgf_files.append(os.path.join(dir,files)) #probably should create a routunes class to abstract his iteration stuff out

    for game_file_paths in sgf_files:
        Analytics(game_file_paths).game_avg_conn()

def test_anim_routine(dir):

    sgf_files = []
    for files in os.listdir(dir):
        if files.endswith(".sgf"):
            sgf_files.append(os.path.join(dir,files)) #probably should create a routunes class to abstract his iteration stuff out

    for game_file_paths in sgf_files:
        GameAnimator(game_file_paths).animate()



def test_scroll_routine(file):

    GameScroll(file).scroll()


if __name__ == '__main__':
  main(sys.argv[1:])

#Test routines
#Animation routines
#Persistence Diagrams?\
#Go analysis features.

#Ideas
#How to interpret H_1 points on DGMS? For example, if a point has a earlier,later birthtime vs earlier,later deathtime? How do we interpret this as properties of possible enclosed territory.
#We can now start to add points to the white/black board to model obstructions to building territory. A good idea would be to find ways to create "meaningful" boards for analysis of specific advantage properties.
#Research more about Go fighting strategies and early,late game caveats
