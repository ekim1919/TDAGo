from plot import GameAnimator,Analytics

import sys
import os

def main(argv):

    test_anim_routine(str(argv[0]))

def run_wass_routine(dir):

    sgf_files = []
    for files in os.listdir(dir):
        if files.endswith(".sgf"):
            sgf_files.append(os.path.join(dir,files)) #probably should create a routunes class to abstract his iteration stuff out

    for game_file_paths in sgf_files:
        Analytics(game_file_paths).game_wdist()

def test_anim_routine(file):

    ani = GameAnimator(file)
    ani.animate()

if __name__ == '__main__':
  main(sys.argv[1:])

#Test routines
#Animation routines
#Persistence Diagrams?\
#Go analysis features.
