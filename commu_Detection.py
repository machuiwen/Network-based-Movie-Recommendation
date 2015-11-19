import snap
import math
import numpy

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
	totalCnt = 0.0
	cumulatedScore = 0.0
	for communityMember in communityResult:
		if (communityMember.IsNIdIn(currentUser)):  # current user is in this community
		   	for nodeMember in communityMember:
		   		if (matrixScore[nodeMember][targetMovie] != 0):
		   			totalCnt = totalCnt + 1
		    		cumulatedScore += matrixSimlarityUser[nodeMember][currentUser] * matrixScore[nodeMember][targetMovie]
	    	if (totalCnt == 0):
	    		return 0    # if none of the community member has watched this movie.
	    	else:
	    		return cumulatedScore * 1.0 / totalCnt

# prediction method 2, Item-Item prediction.
# use the movies in the same movie community
# to apply collaborative filtering to the target movie.
# Two matrix information needed:
# 1. matrixSimlarityMovie: define similartiy of any two movies.
# 2. matrixScore: define score of any user to any movie.
def predictionMethod_2(currentUser, targetMovie, communityResult):
	#if (matrixScore[currentUser][targetMovie] != 0):    # if this user has already rated this movie.
	#	return matrixScore[currentUser][targetMovie]
	totalCnt = 0.0
	cumulatedScore = 0.0
	for communityMember in communityResult:
		if (communityMember.IsNIdIn(targetMovie)):  # current user is in this community
		    for nodeMember in communityMember:
		    	if (matrixScore[currentUser][nodeMember] != 0):
		    		totalCnt = totalCnt + 1
		    		cumulatedScore += matrixSimlarityMovie[targetMovie][nodeMember] * matrixScore[currentUser][nodeMember]
	    	if (totalCnt == 0):
	    		return 0    # if none of the community member has watched this movie.
	    	else:
	    		return cumulatedScore * 1.0 / totalCnt

# system performance test methd;
# input: start and end index for x and y dimension of the utility matrix.
# return: RMSE value.
# matrixScore information is needed: define score of any user to any movie.
def systemTest(xStart, xEnd, yStart, yEnd, communityResult, flag):
	result = 0
	count = 0
	for x in range(xStart, xEnd):
		userID = x
		for y in range(yStart, yEnd):
			movieID = y
			if (matrixScore[userID][movieID] != 0):
				goldScore = matrixScore[userID][movieID]
				if (flag == 1):
					predictedScore = predictionMethod_1(userID, movieID, communityResult)
				else :
					predictedScore = predictionMethod_2(userID, movieID, communityResult)
				result += math.pow((predictedScore - goldScore), 2)
				count += 1.0
	return math.sqrt(result / count)


def main():
	
	UG = snap.GenRndGnm(snap.PUNGraph, 100, 1000)
	MG = snap.GenRndGnm(snap.PUNGraph, 1000, 100000)
	UGcommunityResult = communityDetectionMethod_1(UG)
	MGcommunityResult = communityDetectionMethod_1(MG)
	print systemTest(1, 10, 20, 40, UGcommunityResult, 1)
	print systemTest(1, 10, 20, 40, MGcommunityResult, 2)
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
