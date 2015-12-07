import snap

def buildGraph(threshold, numNodes, matrix):
	# f = open()
	totalEdge = 0
	validEdge = 0
	G = snap.TUNGraph.New()
	for i in range(numNodes):
		G.AddNode(i + 1)

	shape = matrix.shape
	for x in range(shape[0]):
		for y in range(x + 1, shape[1]):
			totalEdge += 1
			if matrix[x][y] > threshold:
				G.AddEdge(x + 1, y + 1)
				validEdge += 1
	print "building graph: totalEdge", totalEdge, " , validEdge", validEdge, ", percentage", validEdge * 1.0 / totalEdge
	return G

def buildGraph_withLabel(th_cos, th_label, numNodes, matrix_cos, matrix_label):
	# f = open()
	totalEdge = 0
	validEdge = 0
	G = snap.TUNGraph.New()
	for i in range(numNodes):
		G.AddNode(i + 1)

	shape = matrix_cos.shape
	for x in range(shape[0]):
		for y in range(x + 1, shape[1]):
			totalEdge += 1
			if matrix_cos[x][y] > th_cos or matrix_label[x][y] >= th_label:
				G.AddEdge(x + 1, y + 1)
				validEdge += 1
	print "building graph: totalEdge", totalEdge, " , validEdge", validEdge, ", percentage", validEdge * 1.0 / totalEdge
	return G

def buildEdgeFile(threshold, numNodes, matrix, filename):
	f = open(filename, 'w')
	for i in range(numNodes):
		f.write(str(i+1) + '\n')

	for x in range(matrix.shape[0]):
		for y in range(x + 1, matrix.shape[1]):
			if matrix[x][y] > threshold:
				f.write(str(x+1) + ',' + str(y+1) + ',' + str(matrix[x][y]) + '\n')
	f.close()

# def generateGraph(filename):
# 	return snap.LoadEdgeList(snap.PUNGraph, filename, 0, 1)



