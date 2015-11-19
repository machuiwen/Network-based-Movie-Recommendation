import snap

f_out = open("UG_0.1_100K_graph.txt", 'w')
G = snap.LoadEdgeList(snap.PUNGraph, "UG_0.1_100K.txt", 0, 1, '\t')
for node in G.Nodes():
	f_out.write(str(node.GetId()) + '\n')

for edge in G.Edges():
	f_out.write(str(edge.GetSrcNId()) + ',' + str(edge.GetDstNId()) + '\n')

f_out.close()


	
