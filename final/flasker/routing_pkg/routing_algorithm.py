'''路径规划算法API'''
import networkx as nx
import numpy as np
import random
import math
from flasker.database.database_link import *


# Dijkstra算法
def dijkstra(graph, startIndex, path, cost, max):
    """
    求解各节点最短路径，获取path，和cost数组，
    path[i] 表示vi节点的前继节点索引，一直追溯到起点。
    cost[i] 表示vi节点的花费
    """
    lenth = len(graph)
    v = [0] * lenth
    # 初始化 path，cost，V
    for i in range(lenth):
        if i == startIndex:
            v[startIndex] = 1
        else:
            cost[i] = graph[startIndex][i]
            path[i] = (startIndex if (cost[i] < max) else -1)
    # print v, cost, path
    for i in range(1, lenth):
        minCost = max
        curNode = -1
        for w in range(lenth):
            if v[w] == 0 and cost[w] < minCost:
                minCost = cost[w]
                curNode = w
        # for 获取最小权值的节点
        if curNode == -1: break
        # 剩下都是不可通行的节点，跳出循环
        v[curNode] = 1
        for w in range(lenth):
            if v[w] == 0 and (graph[curNode][w] + cost[curNode] < cost[w]):
                cost[w] = graph[curNode][w] + cost[curNode]  # 更新权值
                path[w] = curNode  # 更新路径
        # for 更新其他节点的权值（距离）和路径
    return path


# A*算法
def a_star(graph, startIndex, path, cost, max):
    pass

# D*算法（D算法在每次环境状态发生变化时，可以快速地更新路径规划而不需要重新从头开始搜索）
def dijkstra2():
    pass


# 蚁群算法（算法主要利用蚂蚁在觅食过程中释放信息素的原理，信息素浓度高的地方对蚂蚁有较大吸引力，最短路径上的蚂蚁信息素浓度最高，据此可以找到最优路径）
# 看是否可以根据景点信息权重来影响蚁群算法
# 传入距离矩阵和启发函数，返回最优路径的景点索引
# 加UI，“正在为你智能规划路径中”
class AntColonyOptimizer:
    def __init__(self, distances, interests, n_ants, n_best, n_iterations, decay, alpha=1, beta=1, gamma=1):
        self.distances = distances  # 景点之间的距离矩阵
        self.interests = interests  # 每个景点权重
        self.pheromone = np.ones(self.distances.shape) / len(distances)  # 用于存储路径上的信息素浓度。
        self.all_inds = range(len(distances))  # 用于存储所有城市索引
        self.n_ants = n_ants  # 蚂蚁数量
        self.n_best = n_best  # 每次迭代中，选择最好的蚂蚁数量
        self.n_iterations = n_iterations  # 迭代次数
        self.decay = decay  # 信息素衰减因子
        self.alpha = alpha  # 信息素重要程度
        self.beta = beta  # 启发式重要程度
        self.gamma = gamma  # 新增权重的影响因子

    def run(self, start, end):
        shortest_path = None
        best_length = float('inf')
        for _ in range(self.n_iterations):
            all_paths = self.gen_all_paths(start, end)
            self.spread_pheromone(all_paths, self.n_best)
            shortest_path, best_length = self.find_best_path(all_paths, best_length, shortest_path)
            self.pheromone *= self.decay
        if shortest_path is None:
            return None, float('inf')
        return shortest_path, best_length

    def spread_pheromone(self, all_paths, n_best):
        for path, length in all_paths:
            if path is not None:
                for move in path:
                    self.pheromone[move] += 1.0 / self.distances[move]

    def gen_all_paths(self, start, end):
        all_paths = []
        for _ in range(self.n_ants):
            path = self.gen_path(start, end)
            if path is not None:
                all_paths.append((path, self.path_length(path)))
        return all_paths

    def gen_path(self, start, end):
        path = []
        visited = set()
        visited.add(start)
        prev = start
        while prev != end:
            next = self.select_next_city(prev, visited)
            if next is None:
                return None
            path.append((prev, next))
            prev = next
            visited.add(next)
        return path

    def select_next_city(self, current, visited):
        pheromone = np.copy(self.pheromone[current])
        pheromone[list(visited)] = 0
        heuristic = (1.0 / np.where(self.distances[current] > 0, self.distances[current], 1e-10)) * (
                self.interests ** self.gamma)
        row = pheromone ** self.alpha * heuristic ** self.beta
        row_sum = row.sum()
        if row_sum == 0:
            return None
        norm_row = row / row_sum
        if np.any(np.isnan(norm_row)):
            return None
        next_city = np.random.choice(self.all_inds, 1, p=norm_row)[0]
        return next_city

    def path_length(self, path):
        if path is None:
            return float('inf')
        length = 0
        for (start, end) in path:
            length += self.distances[start][end]
        return length

    def find_best_path(self, paths, best_length, best_path):
        for path, length in paths:
            if path is not None and length < best_length:
                best_length = length
                best_path = path
        return best_path, best_length


def ant_colony_optimization(distances, interests, start_index, end_index):
    aco = AntColonyOptimizer(distances, interests, n_ants=10, n_best=5, n_iterations=100, decay=0.95, alpha=1, beta=2,
                             gamma=2)
    shortest_path, length = aco.run(start_index, end_index)
    path = [shortest_path[0][0]]
    for spot in shortest_path:
        if spot[1] != spot[0]:
            path.append(spot[1])
    return path

# 涉及全景点的蚁群算法
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
    start_city = start_id  # 示例起点
    print('start_city', start_city)
    end_city = end_id  # 示例终点
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
    return BestPath  # 输出最优路径