import numpy as np
import random
from flasker.database.database_link import *
import math
import time
'''
可以选择起点和终点，并走过所有点的最优化路线
'''

# def getdistmat(coordinates):
#     numcity = coordinates.shape[0]
#     distmat = np.zeros((numcity, numcity))
#     for i in range(numcity):
#         for j in range(numcity):
#             distmat[i][j] = np.linalg.norm(coordinates[i] - coordinates[j])
#     return distmat
#
#
# # 示例坐标，需根据实际情况替换
# coordinates = np.array([[0, 0], [1, 1], [2, 2], [3, 3]])
# distmat = getdistmat(coordinates)

adjacent_matrix = get_adjacent_matrix()

start_time = time.time()


def allspots_ACO(distmat, start_id, end_id):
    numcity = distmat.shape[0]
    print('景点数量：' + str(numcity))
    # numant = math.ceil(1.5 * numcity)
    numant = 10
    print('蚂蚁数量：' + str(numant))
    alpha = 1
    beta = 5
    rho = 0.05
    Q = 20
    iter = 0
    itermax = 100
    etatable = 1.0 / (distmat + np.diag([1e10] * numcity))
    pheromonetable = np.ones((numcity, numcity))
    pathtable = np.zeros((numant, numcity)).astype(int)
    lengthaver = np.zeros(itermax)
    lengthbest = np.zeros(itermax)
    pathbest = np.zeros((itermax, numcity))

    # 需要事先定义起点和终点
    start_city = get_index_by_id(start_id)  # 示例起点
    print('start_city', start_city)
    end_city = get_index_by_id(end_id)  # 示例终点
    print('end_city', end_city)
    # 初始化时，所有蚂蚁在起点开始
    pathtable[:, 0] = start_city

    while iter < itermax:
        length = np.zeros(numant)  # 初始化路径长度
        for i in range(numant):
            visiting = start_city
            unvisited = set(range(numcity)) - {start_city, end_city}
            for j in range(1, numcity - 1):  # 最后一个城市被预留为终点
                listunvisited = list(unvisited)
                probtrans = np.zeros(len(listunvisited))
                for k in range(len(listunvisited)):
                    probtrans[k] = np.power(pheromonetable[visiting][listunvisited[k]], alpha) * \
                                   np.power(etatable[visiting][listunvisited[k]], beta)
                if sum(probtrans) == 0:
                    k = random.choice(listunvisited)
                else:
                    cumsumprobtrans = (probtrans / sum(probtrans)).cumsum()
                    cumsumprobtrans -= np.random.rand()
                    k = listunvisited[(cumsumprobtrans > 0).argmax()]
                pathtable[i, j] = k
                unvisited.remove(k)
                length[i] += distmat[visiting][k]
                visiting = k

            # 添加从最后一个城市到终点的路径
            pathtable[i, -1] = end_city
            length[i] += distmat[visiting][end_city]

        lengthaver[iter] = length.mean()
        if iter == 0:
            lengthbest[iter] = length.min()
            pathbest[iter] = pathtable[length.argmin()].copy()
        else:
            if length.min() > lengthbest[iter - 1]:
                lengthbest[iter] = lengthbest[iter - 1]
                pathbest[iter] = pathbest[iter - 1].copy()
            else:
                lengthbest[iter] = length.min()
                pathbest[iter] = pathtable[length.argmin()].copy()

        # 更新信息素
        changepheromonetable = np.zeros((numcity, numcity))
        for i in range(numant):
            for j in range(numcity - 1):
                changepheromonetable[pathtable[i, j]][pathtable[i, j + 1]] += Q / distmat[pathtable[i, j]][
                    pathtable[i, j + 1]]
            changepheromonetable[pathtable[i, -2]][pathtable[i, -1]] += Q / distmat[pathtable[i, -2]][pathtable[i, -1]]

        pheromonetable = (1 - rho) * pheromonetable + changepheromonetable

        if iter % 5 == 0:
            print("iter(迭代次数):", iter)
        iter += 1

    path_tmp = pathbest[-1]
    BestPath = [start_city]
    for i in path_tmp:
        if i not in BestPath:
            BestPath.append(int(i))
    # BestPath.append(end_city)
    print(BestPath)  # 输出最优路径


allspots_ACO(adjacent_matrix,133,218)
end_time = time.time()
print('运行时间：'+ str(end_time - start_time))