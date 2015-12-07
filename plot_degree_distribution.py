# from commu_Detection_Jiang_V3 import *
import snap
import matplotlib.pyplot as plt

UG = snap.LoadEdgeList(snap.PUNGraph, 'UG_0.25_1M.txt', 0, 1, ',')
DegToCntV = snap.TIntPrV()
snap.GetDegCnt(UG, DegToCntV)

x = [item.GetVal1() for item in DegToCntV]
y = [item.GetVal2() for item in DegToCntV]
print x
print y
plt.plot(x, y)
plt.savefig("ug_deg_distribution.jpg")

# MG = snap.LoadEdgeList(snap.PUNGraph, 'MG_0.2_1M.txt', 0, 1, ',')
# DegToCntV = snap.TIntPrV()
# snap.GetDegCnt(MG, DegToCntV)

# x = [item.GetVal1() for item in DegToCntV]
# y = [item.GetVal2() for item in DegToCntV]
# print x
# print y
# plt.plot(x, y)
# plt.savefig("mg_deg_distribution.jpg")
