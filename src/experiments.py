from goripser import *
from plot import *

from scipy.integrate import simps
from multiprocessing import Pool, Manager, Lock

import os

def predict_avg_experi(dir,limit):

    sgf_files = []
    for files,_ in zip(os.listdir(dir), range(limit)):
        if files.endswith(".sgf"):
            sgf_files.append(os.path.join(dir,files))

    man = Manager()
    correct_pred = man.Value('i',0)
    l = man.Lock()

    pool = Pool(processes=6)
    for game_file_paths in sgf_files:
        pool.apply_async(predict_worker,args=(game_file_paths,correct_pred,l,))

    pool.close()
    pool.join()

    print("Success Rate For" + dir + ":  " + str(correct_pred.value/len(sgf_files)) + "\n")

def predict_worker(game_file_paths,counter,lock):
    proc = SGFProcessor(game_file_paths)
    x = np.arange(proc.num_of_moves())
    black_conn = []
    white_conn = []

    for _, dgms in proc.filter_game(0,400):
        black_h1, white_h1 = dgms[0][1], dgms[1][1]
        black_mean, white_mean = np.mean(black_h1,axis=0), np.mean(white_h1,axis=0)
        black_conn.append(black_mean[0])
        white_conn.append(white_mean[0])

    score = simps(np.asarray(black_conn) - np.asarray(white_conn),x)
    lock.acquire()
    print("Score for " + game_file_paths + " : " + str(score) + " Winner: " + proc.winner_name + " \n")
    lock.release()

    winner = 'b' if (score < 0) else 'w'
    if winner == proc.winner:
        counter.value += 1


def run_wass_routine(dir):

    sgf_files = []
    for files in os.listdir(dir):
        if files.endswith(".sgf"):
            sgf_files.append(os.path.join(dir,files))

    for game_file_paths in sgf_files:
        Analytics(game_file_paths).game_wdist()

def worker_conn(game_file_paths):
    Analytics(game_file_paths).game_avg_conn()

def run_conn_routine(dir):
    sgf_files = []
    for files in os.listdir(dir):
        if files.endswith(".sgf"):
            sgf_files.append(os.path.join(dir,files))

    #pool = Pool(processes=6)
    for game_file_paths in sgf_files:
        worker_conn(game_file_paths)
    #pool.close()
    #pool.join()

def test_anim_routine(dir):
    """
    sgf_files = []
    for files in os.listdir(dir):
        if files.endswith(".sgf"):
            sgf_files.append(os.path.join(dir,files))

    for game_file_paths in sgf_files:
    """
    GameAnimator(dir).animate()

def test_save_routine(dir):
    sgf_files = []
    for files in os.listdir(dir):
        if files.endswith(".sgf"):
            sgf_files.append(os.path.join(dir,files))

    for game_file_paths in sgf_files:
        SaveGameProg(game_file_paths).plot()


def test_score_routine(dir):
    sgf_files = []
    for files in os.listdir(dir):
        if files.endswith(".sgf"):
            sgf_files.append(os.path.join(dir,files))

    for game_file_paths in sgf_files:
        Analytics(game_file_paths).game_scoring()

def test_scroll_routine(file):
    GameScroll(file).scroll()
