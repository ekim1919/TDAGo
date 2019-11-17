from plot import *

import sys
import os

def main(argv):

    test_scroll_routine(str(argv[0]))

def run_wass_routine(dir):

    sgf_files = []
    for files in os.listdir(dir):
        if files.endswith(".sgf"):
            sgf_files.append(os.path.join(dir,files)) #probably should create a routunes class to abstract his iteration stuff out

    for game_file_paths in sgf_files:
        Analytics(game_file_paths).game_wdist()

def test_anim_routine(file):

    GameAnimator(file).animate()


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
#Create a modular framework such that you have TDA-DATA -> plot modules -> customizable plot figure -> analysis interface
#Create a caching scheme to cache all sequential computations and diagrams made. See cache-tools 
