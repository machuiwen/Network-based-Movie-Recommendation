from numpy import *
import numpy
from scipy.sparse import lil_matrix, csr_matrix
from scipy.io import loadmat
from data_config import *
# import h5py

def generate_ratings_matrix(data):
	"""
	Non sparse
	Matrix format: MAX_USER_ID x MAX_MOVIE_ID
	Return value: matrix
	"""
	ratings_file = open(data['ratings_new'], 'r')
	ratings_mat = zeros((data['MAX_USER_ID'], data['MAX_MOVIE_ID']))
	for lineId, line in enumerate(ratings_file):
		lst = line.split('::')
		user_id = int(eval(lst[0]))
		movie_id = int(eval(lst[1]))
		rating = eval(lst[2])
		ratings_mat[user_id - 1][movie_id - 1] = rating
		if (lineId % 100000 == 0): # max 100_00000
			print lineId
	ratings_file.close()
	return ratings_mat

def generate_ratings_matrix_sparse(data):
	"""
	Sparse
	Return value: matrix
	"""
	ratings_file = open(data['ratings_new'], 'r')
	ratings_mat = lil_matrix((data['MAX_USER_ID'], data['MAX_MOVIE_ID']))
	for lineId, line in enumerate(ratings_file):
		lst = line.split('::')
		user_id = int(eval(lst[0]))
		movie_id = int(eval(lst[1]))
		rating = eval(lst[2])
		ratings_mat[user_id - 1, movie_id - 1] = rating
		if (lineId % 100000 == 0): # max 100_00000
			print lineId
	ratings_file.close()
	# compressed sparse row matrix
	csr = ratings_mat.tocsr()
	return csr

def load_ratings_matrix_from_mat(data):
	"""
	Non sparse, Fast!
	"""
	if (data['size'] == '1M' or data['size'] == '100K'):
		return float32(loadmat(data['ratings_matrix'])['ratings_matrix'])
	# elif (data['size'] == '10M'):		
	# 	mat_file = h5py.File(data['ratings_matrix'], 'r')
	# 	data = mat_file.get('ratings_matrix')
	# 	return float32(numpy.array(data))

def load_mat(filename, key):
	return float32(loadmat(data[filename])[key])

def load_user_similarity(data):
	print "Start loading user similarity"
	return float32(loadmat(data['user_similarity_matrix'])['user_similarity_matrix'])

def load_movie_similarity(data):
	print "Start loading movie similarity"
	return float32(loadmat(data['movie_similarity_matrix'])['movie_similarity_matrix'])


if __name__ == "__main__":
	# stuff only to run when not called via 'import' here
	# generate_ratings_matrix_sparse()
	# m = load_ratings_matrix_from_mat(data_1M)
	# print type(m[0][0])
	print 1
