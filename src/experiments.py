from goripser import *
import os
from scipy.integrate import simps

def predict_avg_experi(dir):

    sgf_files = []
    for files in os.listdir(dir):
        if files.endswith(".sgf"):
            sgf_files.append(os.path.join(dir,files))

    correct_pred = 0
    for game_file_paths in sgf_files:
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

        winner = 'b' if (score >= 0) else 'w'
        if winner == proc.winner:
            correct_pred += 1

    print("Success Rate For" + dir + ":" + str(correct_pred/len(sgf_files)) + "\n")
