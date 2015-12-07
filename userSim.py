import numpy as np
from numpy import *
from data_config import *
from scipy.io import savemat

def getUserSim(F1, F2, weight):
	sim = 0
	weightSum = float(sum(weight))
	weight = [w / weightSum for w in weight]
	# Gender::Age::Occupation::Zip-code
	for i in range(0, len(F1)):
		if F1[i] == F2[i]:
			sim += weight[i]
	return sim

def computeUserSimMatrixFromBioInfo(dataset):
	N = dataset['MAX_USER_ID']
	userFile = open(dataset['users'], 'r')
	users = userFile.readlines()
	userFile.close()
	users = [u.strip().split('::')[1:N] for u in users]
	sim_mat = zeros((N, N))
	for i in range(N - 1):
		if i % 500 == 0:
			print i
		for j in range(i + 1, N):
			sim_mat[i][j] = getUserSim(users[i], users[j], [1,3,2,1])
	sim_mat += np.transpose(sim_mat)
	sim_mat += np.identity(N)
	savemat(file_name=dataset['root']+'userBioSim.mat', mdict={'user_sim_from_bio': sim_mat})

if __name__ == '__main__':
	computeUserSimMatrixFromBioInfo(data_1M)