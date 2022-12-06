import numpy as np

def sim(dj, q):
    result = 0
    dj_norm = np.linalg.norm(dj)
    q_norm = np.linalg.norm(q)
    for i in range(0,min(len(dj),len(q))):
        result +=  dj[i]*q[i]
    return (result / (dj_norm * q_norm))

#term-document matrix
A = np.array([[0,1,1],[1,0,0],[0,1,0],[1,0,0],
              [1,0,1],[1,0,1],[0,2,0],[0,1,1]])
#query vector
q = np.array([0,0,0,0,1,0,1,1])

#performing SVD
T, S, DT = np.linalg.svd(A)

T = np.round(T,4)
S = np.round(S,4)
DT = np.round(DT,4)
print("T: ")
print(T[0:8,0:3])

print("\n")
print("S: ")
print(np.diag(S))
print("\n")
print("DT: ")
print(DT)

#dimensionality reduction
T2 = T[0:8,0:2]
S2 = np.diag(S[0:2])
DT2 = DT[0:2,0:3]

print("\n")
print("T2: ")
print(T2)
print("\n")
print("S2: ")
print(S2)
print("\n")
print("DT2: ")
print(DT2)

#query vector in the reduced 2-dimensional space
q2 = np.dot(np.dot(np.linalg.inv(S2),T2.transpose()),q)

print("\n")
print("q2: ")
print(np.round(q2,4))

#documents vectors in the reduced 2-dimensional space
d1 = np.array([[DT2[0,0]], [DT2[1,0]]])
d2 = np.array([[DT2[0,1]], [DT2[1,1]]])
d3 = np.array([[DT2[0,2]], [DT2[1,2]]])

#Rank documents by calculating the query-document cosine similarities.
sim1 = np.round(sim(d1,q2),4)
sim2 = np.round(sim(d2,q2),4)
sim3 = np.round(sim(d3,q2),4)

print("\nsim(q,d1): ")
print(sim1)
print("\nsim(q,d2): ")
print(sim2)
print("\nsim(q,d3): ")
print(sim3)