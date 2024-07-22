import numpy as np
import random
from recommendation import get_recommendation
import time
from flasker.database.database_link import *

'''
可以根据兴趣生成全景点路径
'''

# 获取邻接矩阵
dismat = get_adjacent_matrix()

# 获取用户兴趣
interests = get_recommendation('users_1')
new_dict = {int(key.split('_')[-1]): value for key, value in interests.items()}
interests = [0] * len(interests)
for key, value in new_dict.items():
    spot_index = get_index_by_id(key)
    interests[spot_index] = value
print(interests)


def allspots_ACO(distmat, start_id, end_id, interest_weights):
    numcity = distmat.shape[0]
    print('景点数量：' + str(numcity))
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

    start_city = get_index_by_id(start_id)
    print('start_city', start_city)
    end_city = get_index_by_id(end_id)
    print('end_city', end_city)
    pathtable[:, 0] = start_city

    while iter < itermax:
        length = np.zeros(numant)
        for i in range(numant):
            visiting = start_city
            unvisited = set(range(numcity)) - {start_city, end_city}
            for j in range(1, numcity - 1):
                listunvisited = list(unvisited)
                probtrans = np.zeros(len(listunvisited))
                for k in range(len(listunvisited)):
                    interest_factor = interest_weights[listunvisited[k]] if interest_weights[listunvisited[k]] > 0 else 0.1
                    probtrans[k] = (np.power(pheromonetable[visiting][listunvisited[k]], alpha) *
                                    np.power(etatable[visiting][listunvisited[k]], beta) *
                                    interest_factor)  # 修改转移概率

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

        changepheromonetable = np.zeros((numcity, numcity))
        for i in range(numant):
            for j in range(numcity - 1):
                changepheromonetable[pathtable[i, j]][pathtable[i, j + 1]] += Q / distmat[pathtable[i, j]][pathtable[i, j + 1]]
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
    print(BestPath)  # 输出最优路径
    print(len(BestPath))


allspots_ACO(dismat, 133, 218, interests)

