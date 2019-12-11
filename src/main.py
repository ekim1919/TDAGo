from plot import *
import warnings
warnings.filterwarnings("ignore") #Ignore warnings for now
import sys
import os
from experiments import *

def main(argv):

    #run_conn_routine(str(argv[0]))
    #predict_avg_experi(str(argv[0]),int(argv[1]))
    test_save_routine(str(argv[0]))
    #test_score_routine(str(argv[0]))
    #$test_anim_routine(str(argv[0]))

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
