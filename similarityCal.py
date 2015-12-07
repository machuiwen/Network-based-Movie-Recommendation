import numpy as np
from scipy import spatial
import math, snap
import sys
from ratings_matrix_generation import *
from data_config import *

def normalizeMatrix_sparse(matrix):
	# print matrix
	sum_all = matrix.sum(1)
	print matrix.shape[0]
	for i in range(matrix.shape[0]):
		row = matrix.getrow(i)
		ave = sum_all[i, 0] / row.size
		# print ave
		denserow = row.toarray()[0]
		# print denserow
		for j in range(denserow.size):
			if denserow[j] != 0:
				matrix[i, j] -= ave

def normalizeMatrix(matrix):
	k = 0
	for row in matrix:
		if k % 1000 == 0:
			print k
		k += 1
		nonzero = np.count_nonzero(row)
		# print len(row), nonzero
		if nonzero == 0:
			continue
		ave = sum(row) * 1.0 / nonzero
		for i in range(len(row)):
			if row[i] != 0:
				tmp = row[i]
				row[i] -= ave
				if row[i] > 5:
					print "### error", row[i], tmp, ave

def cosine_similarity(x1, x2):
	score = 1 - spatial.distance.cosine(x1, x2)
	if score > 1.00001:
		print "cosine score is larger than 1"
		print x1, x2
		print sum(x1 * x2), np.linalg.norm(x1) * np.linalg.norm(x2) 
		print "result = ", sum(x1 * x2) * 1.0 / (np.linalg.norm(x1) * np.linalg.norm(x2))
	return score

# def corre_coef(x1, x2):
# 	index = [i for i in range(min(x1.size, x2.size)) if x1[i] != 0 and x2[i] != 0];
# 	if len(index) == 0:
# 		return 0
# 	y1 = np.array([x1[i] for i in index])
# 	y2 = np.array([x2[i] for i in index])
# 	return sum(y1 * y2) * 1.0 / math.sqrt(sum(y1 * y1) * sum(y2 * y2))

def corre_coef(x1, x2):
	intersection = np.logical_and(x1, x2).astype(float32)
	x1_new = x1 * intersection
	x2_new = x2 * intersection
	if intersection.sum() == 0:
		return 0
	else:
		return cosine_similarity(x1_new, x2_new)

def user_sim_measure_sparse(matrix, threshold, filename):
	out_f = open(filename, 'w')
	print "normalize matrix"
	normalizeMatrix_sparse(matrix)
	print "finish normalizing matrix"
	# print matrix
	rows = matrix.shape[0]
	print "start output user IDs"
	for lineNum in range(rows):
		out_f.write(str(lineNum) + '\n')
	print 'finish output user IDs'

	print 'start calculating similarity'
	for x1 in range(rows):
		if (x1 % 100000== 0): # max 100_00000
			print x1
		row1 = matrix.getrow(x1)
		if row1.size == 0:
			continue
		row1dense = row1.toarray()[0]
		for x2 in range(x1 + 1, rows):
			row2 = matrix.getrow(x2)
			if row2.size == 0:
				continue
			score = cosine_similarity(row1dense, row2.toarray()[0])
			# score = corre_coef(row1dense, row2.toarray()[0])
			print x1+1, x2+1, score
			# if score > threshold:
			out_f.write(str(x1+1) + ',' + str(x2+1) + ',' + str(score) + '\n')
	out_f.close()

def sim_measure(matrix, threshold, filename, filename2):
	# out_f = open(filename, 'w')
	rows = matrix.shape[0]
	# print "rows: ", rows

	# print "start output user IDs"
	# for lineNum in range(rows):
	# 	out_f.write(str(lineNum + 1) + '\n')
	# print 'finish output user IDs'

	print "normalize matrix"
	normalizeMatrix(matrix)
	# print "finish normalizing matrix"
	
	print 'start calculating similarity'
	edge_f = open(filename2, 'w')
	for x1 in range(rows):
		if x1 % 300 == 0: # max 100_00000
			print x1
		row1 = matrix[x1]
		if np.count_nonzero(row1) == 0:
			continue

		for x2 in range(x1 + 1, rows):
			row2 = matrix[x2]
			if np.count_nonzero(row2) == 0:
				continue
			# score = cosine_similarity(row1, row2)
			score = corre_coef(row1, row2)
			# print x1+1, x2+1, score
			# if score > threshold:
			# out_f.write(str(x1+1) + ',' + str(x2+1) + ',' + str(score) + '\n')
			edge_f.write(str(x1+1) + '\t' + str(x2+1) + '\t' + str(score) + '\n')
	edge_f.close()
	# out_f.close()

matrix = load_ratings_matrix_from_mat(data_1M)
print "finish parsing"

# print "start user"
# sim_measure(matrix, 0, "userFull_1M_coef.txt", "userEdge_1M_coef.txt")
print "start movie"
matrix = matrix.transpose()
sim_measure(matrix, 0, "movieFull_1M_coef.txt", "movieEdge_1M_coef.txt")

# x1 = np.array([1,0,2,1,0])
# x2 = np.array([0,1,1,0,1])
# x3 = np.array([2,1,0,1,2])
# print cosine_similarity(x1, x2)
# print cosine_similarity(x1, x3)
# print cosine_similarity(x2, x3)


