from commu_Detection_Jiang_V3 import *
import snap
import matplotlib.pyplot as plt

def thresholdUserLoop():
	# ug_threshold = 0.05
	# mg_threshold = 0.05
	shape = matrixScore.shape
	# print "Calculate benchmark"
	# systemTest(0, shape[0], 0, shape[1], None, 4)

	print "Start looping"
	for threshold in [0.05, 0.1, 0.15, 0.2, 0.25, 0.3]:
	# for threshold in [0]:
		print "*********** Threshold:", threshold, "**************"
		UG_file = "UG_" + str(threshold) + "_" + data['name'] + ".txt"
		# MG_file = "MG_" + str(threshold) + "_" + data['name'] + ".txt"
		if (os.path.isfile(UG_file)):
			UG = snap.LoadEdgeList(snap.PUNGraph, UG_file, 0, 1, '\t')
		else:
			UG = buildGraph(threshold, data['MAX_USER_ID'], matrixSimlarityUser)
			snap.SaveEdgeList(UG, UG_file, "Save as tab-separated list of edges")
		# # snap.PlotInDegDistr(UG, UG_file + "jpg", "degree distribution")
		# DegToCntV = snap.TIntPrV()
		# snap.GetDegCnt(UG, DegToCntV)
		# x = [item.GetVal1() for item in DegToCntV]
		# y = [item.GetVal2() for item in DegToCntV]
		# plt.plot(x, y)
		# plt.savefig(str(threshold) + "deg_distribution.jpg")
		# print "sum_deg", sum(y)

		# if (os.path.isfile(MG_file)):
		# 	MG = snap.LoadEdgeList(snap.PUNGraph, MG_file, 0, 1, '\t')
		# else:
		# 	MG = buildGraph(threshold, data['MAX_MOVIE_ID'], matrixSimlarityMovie)
		# 	snap.SaveEdgeList(MG, MG_file, "Save as tab-separated list of edges")

		print "Load graph done, UG", UG.GetNodes()#, " MG", MG.GetNodes()
		# print "Load graph done, MG", MG.GetNodes()
		UGcommunityResult = communityDetectionMethod_1(UG)
		# print "UG generation done"
		# print "UGcommunityResult: "
		# for com in UGcommunityResult:
		# 	print len(com)
		# MGcommunityResult = communityDetectionMethod_1(MG)
		# print "MG generation done"

		systemTest(0, shape[0], 0, shape[1], UGcommunityResult, 1)
		# systemTest(0, shape[0], 0, shape[1], MGcommunityResult, 2)

def thresholdMovieLoop():
	# ug_threshold = 0.05
	# mg_threshold = 0.05
	shape = matrixScore.shape
	# print "Calculate benchmark"
	# systemTest(0, shape[0], 0, shape[1], None, 4)

	print "Start looping"
	for threshold in [0.4, 0.5]:
	# for threshold in [0]:
		print "*********** Threshold:", threshold, "**************"
		# UG_file = "UG_" + str(threshold) + "_" + data['name'] + ".txt"
		MG_file = "MG_" + str(threshold) + "_" + data['name'] + ".txt"
		# if (os.path.isfile(UG_file)):
		# 	UG = snap.LoadEdgeList(snap.PUNGraph, UG_file, 0, 1, '\t')
		# else:
		# 	UG = buildGraph(threshold, data['MAX_USER_ID'], matrixSimlarityUser)
		# 	snap.SaveEdgeList(UG, UG_file, "Save as tab-separated list of edges")
		# # snap.PlotInDegDistr(UG, UG_file + "jpg", "degree distribution")
		# DegToCntV = snap.TIntPrV()
		# snap.GetDegCnt(UG, DegToCntV)
		# x = [item.GetVal1() for item in DegToCntV]
		# y = [item.GetVal2() for item in DegToCntV]
		# plt.plot(x, y)
		# plt.savefig(str(threshold) + "deg_distribution.jpg")
		# print "sum_deg", sum(y)

		if (os.path.isfile(MG_file)):
			MG = snap.LoadEdgeList(snap.PUNGraph, MG_file, 0, 1, '\t')
		else:
			MG = buildGraph(threshold, data['MAX_MOVIE_ID'], matrixSimlarityMovie)
			snap.SaveEdgeList(MG, MG_file, "Save as tab-separated list of edges")

		# print "Load graph done, UG", UG.GetNodes()#, " MG", MG.GetNodes()
		print "Load graph done, MG", MG.GetNodes()
		# UGcommunityResult = communityDetectionMethod_1(UG)
		# print "UG generation done"
		# print "UGcommunityResult: "
		# for com in UGcommunityResult:
		# 	print len(com)
		MGcommunityResult = communityDetectionMethod_1(MG)
		print "MG generation done"

		# systemTest(0, shape[0], 0, shape[1], UGcommunityResult, 1)
		systemTest(0, shape[0] / 2, 0, shape[1] / 3, MGcommunityResult, 2)

def combineScore(ug_threshold, mg_threshold, beita):
	shape = matrixScore.shape
	# print "Calculate benchmark"
	# systemTest(0, shape[0], 0, shape[1], None, 3)

	# print "*********** Threshold:", threshold, "**************"
	UG_file = "UG_" + str(ug_threshold) + "_" + data['name'] + ".txt"
	MG_file = "MG_" + str(mg_threshold) + "_" + data['name'] + ".txt"
	if (os.path.isfile(UG_file)):
		UG = snap.LoadEdgeList(snap.PUNGraph, UG_file, 0, 1, '\t')
	else:
		UG = buildGraph(ug_threshold, data['MAX_USER_ID'], matrixSimlarityUser)
		snap.SaveEdgeList(UG, UG_file, "Save as tab-separated list of edges")

	if (os.path.isfile(MG_file)):
		MG = snap.LoadEdgeList(snap.PUNGraph, MG_file, 0, 1, '\t')
	else:
		MG = buildGraph(mg_threshold, data['MAX_MOVIE_ID'], matrixSimlarityMovie)
		snap.SaveEdgeList(MG, MG_file, "Save as tab-separated list of edges")
	# snap.PlotInDegDistr(UG, UG_file + "jpg", "degree distribution")
	# DegToCntV = snap.TIntPrV()
	# snap.GetDegCnt(UG, DegToCntV)
	# x = [item.GetVal1() for item in DegToCntV]
	# y = [item.GetVal2() for item in DegToCntV]
	# plt.plot(x, y)
	# plt.savefig(str(threshold) + "deg_distribution.jpg")
	# print "sum_deg", sum(y)

	# if (os.path.isfile(MG_file)):
	# 	MG = snap.LoadEdgeList(snap.PUNGraph, MG_file, 0, 1, '\t')
	# else:
	# 	MG = buildGraph(mg_threshold, data['MAX_MOVIE_ID'], matrixSimlarityMovie)
	# 	snap.SaveEdgeList(MG, MG_file, "Save as tab-separated list of edges")

	print "Load graph done, UG", UG.GetNodes(), " MG", MG.GetNodes()
	UGcommunityResult = communityDetectionMethod_1(UG)
	print "UG generation done"
	# print "UGcommunityResult: "
	# for com in UGcommunityResult:
	# 	print len(com)
	MGcommunityResult = communityDetectionMethod_1(MG)
	print "MG generation done"

	combineSystemTest(0, shape[0], 0, shape[1], UGcommunityResult, MGcommunityResult, beita)
	# systemTest(0, shape[0], 0, shape[1], MGcommunityResult, 2)	

thresholdMovieLoop()
# combineScore(0.1, 0.3, 0.5)