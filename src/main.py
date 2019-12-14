from plot import *
from experiments import *

import warnings
warnings.filterwarnings("ignore") #Ignore warnings for now

import sys
import os
import argparse


def main():
    parser = argparse.ArgumentParser(description='Analysis of Go Games')
    parser.add_argument('dir',nargs='*')
    parser.add_argument('--conn',dest="conn",action='store_true')
    parser.add_argument('--avg',dest="avg",action='store_true')
    parser.add_argument('--score',dest="score",action='store_true')
    parser.add_argument('--anim',dest="anim",action='store_true')

    args = parser.parse_args()
    if args.conn:
        run_conn_routine(args.dir[0])
    if args.avg:
        predict_avg_experi(args.dir[0],args.dir[1])
    if args.score:
        test_score_routine(args.dir[0])
    if args.anim:
        test_anim_routine(args.dir[0])

    #test_save_routine(str(argv[0]))



if __name__ == '__main__':
  main()

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
