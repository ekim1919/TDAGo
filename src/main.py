
import goripser as rip
import sys

def main(argv):
    
    run_wass(int(argv[0]))

def run_wass(game_num):

    dir = "/playpen/ehkim/work/TDAGo/sample_games/Game_00"
    start = 50
    for i in range(1,game_num):
        rip.Analytics(dir + str(i) + ".sgf",start_num=start).game_wdist()

if __name__ == '__main__':
  main(sys.argv[1:])
