# This version added the cost evaluation of diiferent prediction methods.

import snap
import math
import numpy
from data_config import *
from ratings_matrix_generation import *
from scipy.io import loadmat
from graphBuild import *
import os.path

data = data_100K
matrixScore = load_ratings_matrix_from_mat(data)
# matrixSimlarityUser = load_user_similarity(data)
matrixSimlarityMovie = load_movie_similarity(data)
# matrixScore = numpy.random.random((100, 1000))
# matrixSimlarityUser = numpy.random.random((100, 100))
# matrixSimlarityMovie = numpy.random.random((1000, 1000))

def communityDetectionMethod_1(Graph):  
# Uses the Clauset-Newman-Moore community detection method for large networks.
	CmtyV = snap.TCnComV()
	modularity = snap.CommunityCNM(Graph, CmtyV)
	print "Community Dected Num is : ", len(CmtyV)
	return CmtyV

def communityDetectionMethod_2(Graph):  
#   Uses the Girvan-Newman community detection algorithm based on betweenness centrality
	CmtyV = snap.TCnComV()
	modularity = snap.CommunityGirvanNewman(Graph, CmtyV)
	print "Community Dected Num is : ", len(CmtyV)
	return CmtyV

# prediction method 1, User-User Prediction/
# use the users in the same user community
# to apply collaborative filtering to the target movie.
# Two matrix information needed:
# 1. matrixSimlarityUser: define similartiy of any two users.
# 2. matrixScore: define score of any user to any movie.
def predictionMethod_1(currentUser, targetMovie, communityResult):
	#if (matrixScore[currentUser][targetMovie] != 0):    # if this user has already rated this movie.
	#	return matrixScore[currentUser][targetMovie]	
	cumulatedScore = 0.0
	simuSum = 0.0
	totalCnt = 0.0
	for communityMember in communityResult:
		if (communityMember.IsNIdIn(currentUser + 1)):  # current user is in this community
			#print "community has members of: ", communityMember.Len()
			for nodeMember in communityMember:
				if (matrixSimlarityUser[nodeMember - 1][currentUser] > 0 and matrixScore[nodeMember - 1][targetMovie] != 0 and nodeMember - 1 != currentUser):
					totalCnt = totalCnt + 1
					cumulatedScore += matrixSimlarityUser[nodeMember - 1][currentUser] * matrixScore[nodeMember - 1][targetMovie]
					simuSum += matrixSimlarityUser[nodeMember - 1][currentUser]
			if (totalCnt == 0):
				#print "totalCnt = 0"
				return 0, totalCnt    # if none of the community member has watched this movie.
			else:
				return cumulatedScore * 1.0 / simuSum, totalCnt
	return 0, totalCnt


def predictionBenchMark_1(currentUser, targetMovie):
	#if (matrixScore[currentUser][targetMovie] != 0):    # if this user has already rated this movie.
	#	return matrixScore[currentUser][targetMovie]
	totalCnt = 0.0
	cumulatedScore = 0.0
	simuSum = 0.0
	for user in range(0, matrixScore.shape[0]):
		if (user == currentUser):
			continue
		elif (matrixScore[user][targetMovie] != 0 and matrixSimlarityUser[user][currentUser] > 0):
			cumulatedScore += matrixScore[user][targetMovie] * matrixSimlarityUser[user][currentUser]
			totalCnt += 1
			simuSum += matrixSimlarityUser[user][currentUser]
	if (totalCnt == 0):
		return 0, totalCnt
	else:
		return cumulatedScore * 1.0 / simuSum, totalCnt

# prediction method 2, Item-Item prediction.
# use the movies in the same movie community
# to apply collaborative filtering to the target movie.
# Two matrix information needed:
# 1. matrixSimlarityMovie: define similartiy of any two movies.
# 2. matrixScore: define score of any user to any movie.
def predictionMethod_2(currentUser, targetMovie, communityResult):
	#if (matrixScore[currentUser][targetMovie] != 0):    # if this user has already rated this movie.
	#	return matrixScore[currentUser][targetMovie]
	cumulatedScore = 0.0
	simuSum = 0.0
	totalCnt = 0.0
	for communityMember in communityResult:
		if (communityMember.IsNIdIn(targetMovie + 1)):  # current user is in this community
			for nodeMember in communityMember:
				if (matrixSimlarityMovie[targetMovie][nodeMember - 1] > 0 and matrixScore[currentUser][nodeMember - 1] != 0 and nodeMember - 1 != targetMovie):
					totalCnt = totalCnt + 1
					cumulatedScore += matrixSimlarityMovie[targetMovie][nodeMember - 1] * matrixScore[currentUser][nodeMember - 1]
					simuSum += matrixSimlarityMovie[targetMovie][nodeMember - 1] 
			if (totalCnt == 0):
				return 0, totalCnt    # if none of the community member has watched this movie.
			else:
				return cumulatedScore * 1.0 / simuSum, totalCnt
	return 0, totalCnt


def predictionBenchMark_2(currentUser, targetMovie):
	#if (matrixScore[currentUser][targetMovie] != 0):    # if this user has already rated this movie.
	#	return matrixScore[currentUser][targetMovie]
	totalCnt = 0.0
	cumulatedScore = 0.0
	simuSum = 0.0
	for movie in range(0, matrixScore.shape[1]):
		if (movie == targetMovie):
			continue
		elif (matrixScore[currentUser][movie] != 0 and matrixSimlarityMovie[targetMovie][movie] > 0):
			cumulatedScore += matrixScore[currentUser][movie] * matrixSimlarityMovie[targetMovie][movie]
			totalCnt += 1
			simuSum += matrixSimlarityMovie[targetMovie][movie]
	if (totalCnt == 0):
		return 0, totalCnt
	else:
		return cumulatedScore * 1.0 / simuSum, totalCnt


def predictionMethod_3(currentUser, targetMovie, UGcommunityResult, MGcommunityResult, beita):
	score_user = predictionMethod_1(currentUser, targetMovie, UGcommunityResult)
	score_movie = predictionMethod_2(currentUser, targetMovie, MGcommunityResult)
	if score_user[0] == 0:
		return score_movie[0]
	if score_movie[0] == 0:
		return score_user[0]
	return beita * score_user[0] + (1 - beita) * score_movie[0]
# system performance test methd;
# input: start and end index for x and y dimension of the utility matrix.
# return: RMSE value.
# matrixScore information is needed: define score of any user to any movie.
def systemTest(xStart, xEnd, yStart, yEnd, communityResult, flag):
	result = 0
	benchmark_result = 0
	count = 0
	neighborUsed = 0
	neighborUsedSum = 0
	benchmarkNeighborSum = 0
	for x in range(xStart, xEnd):
		if x % 500 == 0:
			print "processing", x
		# userID =
		for y in range(yStart, yEnd):
			# movieID = y
			if (matrixScore[x][y] != 0):
				goldScore = matrixScore[x][y]
				if (flag == 1):
					predictedScore, neighborUsed = predictionMethod_1(x, y, communityResult)
					if (predictedScore != 0):
						benchmarkScore, benchmarkNeighbor = predictionBenchMark_1(x, y)
				elif (flag == 2) :
					predictedScore, neighborUsed = predictionMethod_2(x, y, communityResult)
					if (predictedScore != 0):
						benchmarkScore, benchmarkNeighbor = predictionBenchMark_2(x, y)
				# elif (flag == 3):
				# 	predictedScore, neighborUsed = predictionBenchMark_1(x, y)
				# elif (flag == 4):
				# 	predictedScore, neighborUsed = predictionBenchMark_2(x, y)
				if (predictedScore == 0):
					continue
				result += math.pow((predictedScore - goldScore), 2)
				benchmark_result += math.pow((benchmarkScore - goldScore), 2)
				#if (flag == 2):
				#	print flag, predictedScore, goldScore, neighborUsed
				count += 1.0
				neighborUsedSum += neighborUsed
				benchmarkNeighborSum += benchmarkNeighbor
	if (count == 0):
		return 0, 0
	else:
		print "Valid Data Ratio with flag of " + str(flag) + " is : ", count
		print "System RMSE with flag of " + str(flag) + " is : ", math.sqrt(result / count)
		print "System Cost with flag of " + str(flag) + " is : ", neighborUsedSum * 1.0 / count
		print "Benchmark RMSE with flag of " + str(flag) + " is : ", math.sqrt(benchmark_result / count)
		print "Benchmark cost with flag of " + str(flag) + " is : ", benchmarkNeighborSum * 1.0 / count
		print "-----------------------------------"
		return math.sqrt(result / count), neighborUsedSum

def combineSystemTest(xStart, xEnd, yStart, yEnd, community_usr, community_mv, beita):
	result = 0
	# benchmark_result = 0
	count = 0
	neighborUsed = 0
	neighborUsedSum = 0
	# benchmarkNeighborSum = 0
	for x in range(xStart, xEnd):
		# userID =
		for y in range(yStart, yEnd):
			# movieID = y
			if (matrixScore[x][y] != 0):
				goldScore = matrixScore[x][y]
				predictedScore = predictionMethod_3(x, y, community_usr, community_mv, beita)
				if predictedScore == 0:
					continue
				result += math.pow((predictedScore - goldScore), 2)
				count += 1.0
				# neighborUsedSum += neighborUsed
				# benchmarkNeighborSum += benchmarkNeighbor
	if (count == 0):
		return 0, 0
	else:
		print "Valid Data Ratio is : ", count
		print "System RMSE is : ", math.sqrt(result / count)
		# print "System Cost with flag of " + str(flag) + " is : ", neighborUsedSum * 1.0 / count
		# print "Benchmark RMSE with flag of " + str(flag) + " is : ", math.sqrt(benchmark_result / count)
		# print "Benchmark cost with flag of " + str(flag) + " is : ", benchmarkNeighborSum * 1.0 / count
		print "-----------------------------------"
		return math.sqrt(result / count)


def checkMatrix():
	cnt = 0
	for row in range(0, matrixScore.shape[0]):
		for col in range(0, matrixScore.shape[1]):
			if (matrixScore[row][col] != 0):
				cnt += 1
	print cnt

def main():
	ug_threshold = 0.05
	mg_threshold = 0.05
	# UG = snap.GenRndGnm(snap.PUNGraph, 100, 3000)
	# MG = snap.GenRndGnm(snap.PUNGraph, 1000, 2000)
	print "Start building graph"

	UG_file = "UG_" + str(ug_threshold) + "_" + data['name'] + ".txt"
	MG_file = "MG_" + str(mg_threshold) + "_" + data['name'] + ".txt"
	buildEdgeFile(0.3, data['MAX_MOVIE_ID'], matrixSimlarityMovie, "MG_0.3_100K_graph.txt")
	# buildEdgeFile(0.1, data['MAX_USER_ID'], matrixSimlarityUser, "UG_0._100K_graph.txt")

	# if (os.path.isfile(UG_file)):
	# 	UG = snap.LoadEdgeList(snap.PUNGraph, UG_file, 0, 1, '\t')
	# else:
	# 	UG = buildGraph(ug_threshold, data['MAX_USER_ID'], matrixSimlarityUser)
	# snap.SaveEdgeList(UG, UG_file, "Save as tab-separated list of edges")
	# if (os.path.isfile(MG_file)):
	# 	MG = snap.LoadEdgeList(snap.PUNGraph, MG_file, 0, 1, '\t')
	# else:
	# 	MG = buildGraph(mg_threshold, data['MAX_MOVIE_ID'], matrixSimlarityMovie)
	# 	snap.SaveEdgeList(MG, MG_file, "Save as tab-separated list of edges")
	# print "Load graph done, UG", UG.GetNodes(), " MG", MG.GetNodes()
	# UGcommunityResult = communityDetectionMethod_1(UG)
	# print "UG generation done"
	# MGcommunityResult = communityDetectionMethod_1(MG)
	# print "MG generation done"

	#print "UGcommunityResult: "
	#for com in UGcommunityResult:
	#	print len(com)
	#print "MGcommunityResult: "
	#for com in MGcommunityResult:
	#	print len(com)
	# xStart Index of systemTest start from 0.
	# print "threshold", ug_threshold, mg_threshold
	# systemTest(0, 200, 0, 500, UGcommunityResult, 1)
	# # systemTest(0, matrixScore.shape[0], 0, 100, UGcommunityResult, 3)
	# systemTest(0, 200, 0, 500, MGcommunityResult, 2)
	# systemTest(0, matrixScore.shape[0], 0, 100, MGcommunityResult, 4)
	#print matrixScore.shape[0], matrixScore.shape[1]
	#print systemTest(1, 500, 1, 550, MGcommunityResult, 2)
	#print systemTest(1, 500, 1, 550, MGcommunityResult, 4)
	#print predictionMethod_2(10, 20, MGcommunityResult)
	#print systemTest(1, 10, 20, 40, UGcommunityResult, ScoreMatrix, UserSimMatrix, 1)
	#print systemTest(1, 10, 20, 40, UGcommunityResult, ScoreMatrix, MovieSimMatrix, 2)
	#print predictionMethod_2(10, 20, MGcommunityResult, ScoreMatrix, MovieSimMatrix)
	#print "Community Dected Num is : ", len(communityResult)
	#systemTest(1,5,2,4)
	#currentUser = 10
	#targetMovie = 20
	#predictionMethod_1(currentUser, targetMovie, communityResult)

main()
#checkMatrix()