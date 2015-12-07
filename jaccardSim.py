from data_config import *
from numpy import *
from scipy.io import savemat
def jaccardSim(label1, label2):  
# return the Jaccard Similarity of the two input bag of words.
	bag1 = set(label1.lower().split("|"))
	bag2 = set(label2.lower().split("|"))
	return len(bag1.intersection(bag2)) * 1.0 / len(bag1.union(bag2))

def computeJaccardSimMatrixForMovie(dataset):
	N = dataset['MAX_MOVIE_ID']
	movieFile = open(dataset['movies_new'], 'r')
	movies = movieFile.readlines()
	movieFile.close()
	movies = [m.strip().split('::')[-1] for m in movies]
	sim_mat = zeros((N, N))
	for i in range(N - 1):
		if i % 500 == 0:
			print i
		for j in range(i + 1, N):
			sim_mat[i][j] = jaccardSim(movies[i], movies[j])
	savemat(file_name='jaccardSimMovie.mat', mdict={'mov_sim_from_type': sim_mat})

if __name__ == '__main__':
	computeJaccardSimMatrixForMovie(data_1M)