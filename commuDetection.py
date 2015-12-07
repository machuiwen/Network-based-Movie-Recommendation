# This version added the cost evaluation of diiferent prediction methods.

import snap
import math
import numpy
from data_config import *
from ratings_matrix_generation import *
from scipy.io import loadmat
from graphBuild import *
import os.path

data = data_1M
matrixScore = load_ratings_matrix_from_mat(data)
matrixSimlarityUser = load_user_similarity(data)
matrixSimlarityMovie = load_movie_similarity(data)
matrixLabelMovie = load_movie_similarity(data, 'mov_sim_from_type')
matrixLabelUser = load_user_similarity_bio(data)
global testedBoolMatrix  # to indicate whether data is tested or not.
#global systemPer # system overall performance

# w1 = 1        # weight for original movie-to-movie matrix.
# w2 = 1 - w1   # weight for label based movie-to-movie.


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
def predictionMethod_1(currentUser, targetMovie, communityResult, matrixInput):
	#if (matrixScore[currentUser][targetMovie] != 0):    # if this user has already rated this movie.
	#	return matrixScore[currentUser][targetMovie]	
	cumulatedScore = 0.0
	simuSum = 0.0
	totalCnt = 0.0
	for communityMember in communityResult:
		if (communityMember.IsNIdIn(currentUser + 1)):  # current user is in this community
			#print "community has members of: ", communityMember.Len()
			for nodeMember in communityMember:
				if (matrixInput[nodeMember - 1][currentUser] > 0 and matrixScore[nodeMember - 1][targetMovie] != 0 and nodeMember - 1 != currentUser):
					totalCnt = totalCnt + 1
					cumulatedScore += matrixInput[nodeMember - 1][currentUser] * matrixScore[nodeMember - 1][targetMovie]
					simuSum += matrixInput[nodeMember - 1][currentUser]
			if (totalCnt == 0):
				#print "totalCnt = 0"
				return 0, totalCnt    # if none of the community member has watched this movie.
			else:
				return cumulatedScore * 1.0 / simuSum, totalCnt
	return 0, totalCnt


def predictionBenchMark_1(currentUser, targetMovie, matrixInput):
	#if (matrixScore[currentUser][targetMovie] != 0):    # if this user has already rated this movie.
	#	return matrixScore[currentUser][targetMovie]
	totalCnt = 0.0
	cumulatedScore = 0.0
	simuSum = 0.0
	for user in range(0, matrixScore.shape[0]):
		if (user == currentUser):
			continue
		elif (matrixScore[user][targetMovie] != 0 and matrixInput[user][currentUser] > 0):
			cumulatedScore += matrixScore[user][targetMovie] * matrixInput[user][currentUser]
			totalCnt += 1
			simuSum += matrixInput[user][currentUser]
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
def predictionMethod_2(currentUser, targetMovie, communityResult, matrixInput):
	#if (matrixScore[currentUser][targetMovie] != 0):    # if this user has already rated this movie.
	#	return matrixScore[currentUser][targetMovie]

	cumulatedScore = 0.0
	simuSum = 0.0
	totalCnt = 0.0
	for communityMember in communityResult:
		if (communityMember.IsNIdIn(targetMovie + 1)):  # current user is in this community
			for nodeMember in communityMember:
				if (matrixInput[targetMovie][nodeMember - 1] > 0 and matrixScore[currentUser][nodeMember - 1] != 0 and nodeMember - 1 != targetMovie):
					totalCnt = totalCnt + 1
					weight = matrixInput[targetMovie][nodeMember - 1]
					cumulatedScore += weight * matrixScore[currentUser][nodeMember - 1]
					simuSum += weight
			if (totalCnt == 0):
				return 0, totalCnt    # if none of the community member has watched this movie.
			else:
				return cumulatedScore * 1.0 / simuSum, totalCnt
	return 0, totalCnt


def predictionBenchMark_2(currentUser, targetMovie, matrixInput):
	#if (matrixScore[currentUser][targetMovie] != 0):    # if this user has already rated this movie.
	#	return matrixScore[currentUser][targetMovie]
	totalCnt = 0.0
	cumulatedScore = 0.0
	simuSum = 0.0
	for movie in range(0, matrixScore.shape[1]):
		if (movie == targetMovie):
			continue
		elif (matrixScore[currentUser][movie] != 0 and matrixInput[targetMovie][movie] > 0):
			weight = matrixInput[targetMovie][movie]
			cumulatedScore += weight * matrixScore[currentUser][movie]
			totalCnt += 1
			simuSum += weight
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
def systemTest(testedBoolMatrix, xStart, xEnd, yStart, yEnd, communityResult, flag, matrixInput):
	result = 0
	benchmark_result = 0
	benchmarkScore = 0
	benchmarkNeighbor = 0
	count = 0
	neighborUsed = 0
	neighborUsedSum = 0
	benchmarkNeighborSum = 0
	for x in range(xStart, xEnd):
		#if x % 100 == 0:
		#	print "processing", x
		# userID =
		for y in range(yStart, yEnd):
			# movieID = y
			if (testedBoolMatrix[x][y] == 0):
				continue
			if (matrixScore[x][y] != 0):
				goldScore = matrixScore[x][y]
				if (flag == 1):
					predictedScore, neighborUsed = predictionMethod_1(x, y, communityResult, matrixInput)
					if (predictedScore != 0):
						benchmarkScore, benchmarkNeighbor = predictionBenchMark_1(x, y, matrixInput)
				elif (flag == 2) :
					predictedScore, neighborUsed = predictionMethod_2(x, y, communityResult, matrixInput)
					if (predictedScore != 0):
						benchmarkScore, benchmarkNeighbor = predictionBenchMark_2(x, y, matrixInput)
				# elif (flag == 3):
				# 	predictedScore, neighborUsed = predictionBenchMark_1(x, y)
				# elif (flag == 4):
				# 	predictedScore, neighborUsed = predictionBenchMark_2(x, y)
				if (predictedScore == 0):
					continue

				testedBoolMatrix[x][y] = 0 # mark this data as already tested.
				result += math.pow((predictedScore - goldScore), 2)
				benchmark_result += math.pow((benchmarkScore - goldScore), 2)
				#if (flag == 2):
				#	print flag, predictedScore, goldScore, neighborUsed
				count += 1.0
				neighborUsedSum += neighborUsed
				benchmarkNeighborSum += benchmarkNeighbor
	if (count == 0):
		return 0, 0, 0, 0, 0
	else:
		print "Valid Data Ratio with flag of " + str(flag) + " is : ", count
		print "System RMSE with flag of " + str(flag) + " is : ", math.sqrt(result / count)
		print "System Cost with flag of " + str(flag) + " is : ", neighborUsedSum * 1.0 / count
		print "Benchmark RMSE with flag of " + str(flag) + " is : ", math.sqrt(benchmark_result / count)
		print "Benchmark cost with flag of " + str(flag) + " is : ", benchmarkNeighborSum * 1.0 / count
		print "-----------------------------------"
		#print testedBoolMatrix
		return result, count, neighborUsedSum, benchmarkNeighborSum, benchmark_result

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

def checkValidData(xStart, xEnd, yStart, yEnd):
	result = 0
	for x in range(xStart, xEnd):
		for y in range(yStart, yEnd):
			if (matrixScore[x][y] != 0):
				result += 1
	return result

def checkMatrix():
	cnt = 0
	for row in range(0, matrixScore.shape[0]):
		for col in range(0, matrixScore.shape[1]):
			if (matrixScore[row][col] != 0):
				cnt += 1
	print cnt

def getSystemPer (xStart, xEnd, yStart, yEnd, result, count, testedBoolMatrix):
	count[4] = 0
	result[4] = 0
	for x in range(xStart, xEnd):
		for y in range(yStart, yEnd):
			if (matrixScore[x][y] != 0 and testedBoolMatrix[x][y] == 1):
				# this data can be predicted but not yet.
				count[4] += 1
				result[4] += math.pow((naivePredict(x, y) - matrixScore[x][y]), 2)
	return math.sqrt(sum(result) * 1.0 / sum(count)), result[4], count[4]

def naivePredict(x, y):
	return 3;
	# count = 0
	# result = 0
	# for cnt in range(0, matrixScore.shape[1]):
	# 	if cnt == y:
	# 		continue
	# 	if (matrixScore[x][cnt] != 0):
	# 		count += 1
	# 		result += matrixScore[x][cnt]
	# return result * 1.0 / count

def main():
	ug_threshold = 0.3   # layer 2, 0.15
	mg_threshold = 0.1   # layer 1, 0.2
	ug_label_th = 0.5  # layer 4, 0.1
	mg_label_th = -1  # layer 3, 0.5
	# UG = snap.GenRndGnm(snap.PUNGraph, 100, 3000)
	# MG = snap.GenRndGnm(snap.PUNGraph, 1000, 2000)
	print "Start building graph"

	# UG_file = "UG_" + str(ug_threshold) + "_" + data['name'] + ".txt"
	# MG_file = "MG_" + str(mg_threshold) + "_" + data['name'] + ".txt"
	# buildEdgeFile(0.3, data['MAX_MOVIE_ID'], matrixSimlarityMovie, "MG_0.3_100K_graph.txt")
	# buildEdgeFile(0.1, data['MAX_USER_ID'], matrixSimlarityUser, "UG_0._100K_graph.txt")

	# if (os.path.isfile(UG_file)):
	# 	UG = snap.LoadEdgeList(snap.PUNGraph, UG_file, 0, 1, '\t')
	# else:
	# 	UG = buildGraph_withLabel(ug_threshold, data['MAX_USER_ID'], matrixSimlarityUser, matrixLabelMovie)
	# snap.SaveEdgeList(UG, UG_file, "Save as tab-separated list of edges")
	# if (os.path.isfile(MG_file)):
	# 	MG = snap.LoadEdgeList(snap.PUNGraph, MG_file, 0, 1, '\t')
	# else:
	# 	MG = buildGraph_withLabel(mg_threshold, mg_label_th, data['MAX_MOVIE_ID'], matrixSimlarityMovie, matrixLabelMovie)
	# 	snap.SaveEdgeList(MG, MG_file, "Save as tab-separated list of edges")
	

	MG = buildGraph(mg_threshold, data['MAX_MOVIE_ID'], matrixSimlarityMovie)
	UG = buildGraph(ug_threshold, data['MAX_USER_ID'], matrixSimlarityUser)
	LabelMG = buildGraph(mg_label_th, data['MAX_MOVIE_ID'], matrixLabelMovie)
	LabelUG = buildGraph(ug_label_th, data['MAX_USER_ID'], matrixLabelUser)
	MGcommunityResult = communityDetectionMethod_1(MG)
	UGcommunityResult = communityDetectionMethod_1(UG)
	LabelMGcommunityResult = communityDetectionMethod_1(LabelMG)
	LabelUGcommunityResult = communityDetectionMethod_1(LabelUG)
	#print "Info: ****"
	print "--------- Graph Generation Engine Information ---------"
	#print "mg_threshold:", mg_threshold, " mg_label_th", mg_label_th
	print "movie graph nodes:", MG.GetNodes(), "movie graph edge:", MG.GetEdges()
	print "user graph nodes:", UG.GetNodes(), "user graph edge:", UG.GetEdges()
	print "label based MG nodes:", LabelMG.GetNodes(), "label based MG edge:", LabelMG.GetEdges()
	print "label based UG nodes:", LabelUG.GetNodes(), "label based UG edge:", LabelUG.GetEdges()
	
	# print "Load graph done, UG", UG.GetNodes(), " MG", MG.GetNodes()
	# UGcommunityResult = communityDetectionMethod_1(UG)
	# print "UG generation done"
	
	print "--------- Community Detection Engine Information ---------"
	print "MG generation done, community number", len(MGcommunityResult)
	print "UG generation done, community number", len(UGcommunityResult)
	print "Label based MG generation done, community number", len(LabelMGcommunityResult)
	print "Label based UG generation done, community number", len(LabelUGcommunityResult)

	# print "UGcommunityResult: "
	# for com in UGcommunityResult:
	# 	print len(com)
	# print "MGcommunityResult: "
	# for com in MGcommunityResult:
	#	print len(com)
	#xStart Index of systemTest start from 0.
	# print "threshold", ug_threshold, mg_threshold
	# systemTest(0, 200, 0, 500, UGcommunityResult, 1)
	# # systemTest(0, matrixScore.shape[0], 0, 100, UGcommunityResult, 3)
	print "--------- Score Prediction Engine Information ---------"
	xStart = 0
	xEnd = 500  # max 8000
	yStart = 0
	yEnd = 500 # max 3000
	testedBoolMatrix = [[1 for y in range(yStart, yEnd)] for x in range(xStart, xEnd)]
	result = [0, 0, 0, 0, 0] # 4 layer plus naive prediction.
	benchResult = [0, 0, 0, 0, 0] # 4 layer plus naive prediction.
	count = [0, 0, 0, 0, 0]
	ourCost = [0, 0, 0, 0, 0]
	benchCost = [0, 0, 0, 0, 0]
	# boolean matrix to indicate data tested or not.
	print "--------- Threshold Information ---------"
	print "ug_threshold, mg_threshold, ug_label_th, mg_label_th", ug_threshold, mg_threshold, ug_label_th, mg_label_th

	print "\n--------- User-to-User Vector (Layer 2) ---------"
	matrixInput = matrixSimlarityUser  # user vector based prediction.
	result[1], count[1], ourCost[1], benchCost[1], benchResult[1] = systemTest(testedBoolMatrix, xStart, xEnd, yStart, yEnd, UGcommunityResult, 1, matrixInput)	
	sysPerLayer2, result[4], count[4] = getSystemPer(xStart, xEnd, yStart, yEnd, result, count, testedBoolMatrix)
	print "Layer 1 + 2 System Performance is : ", sysPerLayer2
	naiveRMSE = -1
	if (count[4] != 0):
		naiveRMSE = math.sqrt(result[4] * 1.0 / count[4])
	print "Naive Prediction Performance is : ", naiveRMSE

	print "\n--------- Movie-to-Movie Vector (Layer 1) ---------"
	matrixInput = matrixSimlarityMovie  # user vector based prediction.
	result[0], count[0], ourCost[0], benchCost[0], benchResult[0] = systemTest(testedBoolMatrix, xStart, xEnd, yStart, yEnd, MGcommunityResult, 2, matrixInput)
	sysPerLayer1, result[4], count[4] = getSystemPer(xStart, xEnd, yStart, yEnd, result, count, testedBoolMatrix)
	naiveRMSE = -1
	if (count[4] != 0):
		naiveRMSE = math.sqrt(result[4] * 1.0 / count[4])
	print "Layer 1 System Performance is : ", sysPerLayer1
	print "Naive Prediction Performance is : ", naiveRMSE
	
	
	print "\n--------- Movie Label based (Layer 3) ---------"
	matrixInput = matrixLabelUser  # label based prediction.
	result[3], count[3], ourCost[3], benchCost[3], benchResult[3] = systemTest(testedBoolMatrix, xStart, xEnd, yStart, yEnd, LabelUGcommunityResult, 1, matrixInput)	
	sysPerLayer3, result[4], count[4] = getSystemPer(xStart, xEnd, yStart, yEnd, result, count, testedBoolMatrix)
	print "Layer 1 + 2 + 3 System Performance is : ", sysPerLayer3
	naiveRMSE = -1
	if (count[4] != 0):
		naiveRMSE = math.sqrt(result[4] * 1.0 / count[4])
	print "Naive Prediction Performance is : ", naiveRMSE

	print "\n--------- User Label based (Layer 4) ---------"
	matrixInput = matrixLabelMovie  # label based prediction.
	result[2], count[2], ourCost[2], benchCost[2], benchResult[2] = systemTest(testedBoolMatrix, xStart, xEnd, yStart, yEnd, LabelMGcommunityResult, 2, matrixInput)	

	# print "\n--------- Naive Average based (Layer Final, will predict all the data) ---------"
	# sysPer, result[4], count[4] = getSystemPer(xStart, xEnd, yStart, yEnd, result, count, testedBoolMatrix)
	# naiveRMSE = -1
	# if (count[4] != 0):
	# 	naiveRMSE = math.sqrt(result[4] * 1.0 / count[4])
	# print "Naive Preiction RMSE is (-1 means naive method not used): ", naiveRMSE

	result[4] = 0
	count[4] = 0
	sysPer = math.sqrt(sum(result) * 1.0 / sum(count))
	
	print "\n--------- System Overall Performance ---------"
	print "System Overall Perforamcne is: ", sysPer 
	print "System Benchmark Perforamcne is: ", math.sqrt(sum(benchResult) * 1.0 / (sum(count) - count[4]))
	print "System Overall Cost is: ", sum(ourCost) * 1.0 / (sum(count) - count[4])
	print "System Benchmark Cost is: ", sum(benchCost) * 1.0 / (sum(count) - count[4])

	print "\n--------- Predicted Data Information ---------"
	print "Total data possible for prediction: ", checkValidData(xStart, xEnd, yStart, yEnd)
	print "Total data predicted with first 4 layers: ", sum(count) - count[4]
	print "Total data predicted with 5 layers: ", sum(count)
	
main()
#checkMatrix()