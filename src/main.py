
import goripser as rip
import sys

def main(argv):

    #analy = rip.Analytics(argv[0])
    #analy.game_wdist()
    save_wass(int(argv[0]))

def save_wass(game_num):

    dir = "/playpen/ehkim/work/TDAGo/sample_games/Game_0"

    for i in range(10,game_num):
        rip.Analytics(dir + str(i) + ".sgf").game_wdist()


if __name__ == '__main__':
  main(sys.argv[1:])
