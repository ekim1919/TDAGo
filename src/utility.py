class Plotter:

    def __init__(self, processor):
        self.processor = processor


    def plot_move(self, move_num):

            plt.figure(figsize=(150,30))

            black_stones, white_stones, black_dgms, white_dgms = (self.processor).process_sgf_file(move_num)

            plt.subplot(331)
            plt.xticks(np.arange(20))
            plt.scatter(white_stones[:,0], white_stones[:,1], color='red')
            plt.title('White Stone Positions')

            plt.subplot(332)
            plt.title('White PH')
            plot_diagrams(white_dgms)

            plt.subplot(336)
            plt.scatter(black_stones[:,0], black_stones[:,1],color='black')
            plt.scatter(white_stones[:,0], white_stones[:,1], color='red')
            plt.title('Total Board')

            plt.subplot(337)
            plt.xticks(np.arange(20))
            plt.scatter(black_stones[:,0], black_stones[:,1], color='black')
            plt.title('Black Stone Positions')
            plt.subplot(338)
            plt.title('Black PH')
            plot_diagrams(black_dgms)

            plt.show()

    #Plots wasserstein matching between two consec moves for both colors
    def plot_wass_match(self, move_num):

        plt.figure(figsize=(150,30))

        _,_, bdgms1, wdgms1 = (self.processor).process_sgf_file(move_num)
        #_,_, bdgms2, wdgms2 = (self.processor).process_sgf_file(move_num+20)

        wdist, (match,_) = TDATools.match_wasserstein(wdgms1,bdgms1)

        plt.subplot(122)
        wasserstein_matching(wdgms1[1], bdgms1[1], match)
        plt.title("Matching for Move %i"%move_num)
        print(wdist)

        plt.show()
