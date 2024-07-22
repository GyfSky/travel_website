import numpy as np
'''
可选择起点和终点，并包括用户兴趣的蚁群规划算法
'''

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


# Example usage:
# max = np.inf
# distances = np.array([
#     [max, max, 10, max, 30, 100],
#     [max, max, 5, max, max, max],
#     [max, max, max, 50, max, max],
#     [max, max, max, max, max, 10],
#     [max, max, max, 20, max, 60],
#     [max, max, max, max, max, max],
# ])
#
# interests = np.array([1.0, 1.2, 0.8, 1.5, 2.0, 0.])  # 权重较高的景点更吸引蚂蚁,且权重数量必须与distances的行数相等

max = np.inf
distances = np.array([
    [max, 10, 20, max, max, max],
    [10, max, max, 20, 10, max],
    [20, max, max, 50, max, 30],
    [max, 20, max, max, max, 20],
    [max, 10, max, max, max, 20],
    [max, max, 30, 20, 20, max],
])
interests = np.array([0.5, 0.5, 0.6, 1, 0.3, 0.5])

aco = AntColonyOptimizer(distances, interests, n_ants=10, n_best=5, n_iterations=100, decay=0.95, alpha=1, beta=3,
                         gamma=2)
start_node = 0
end_node = 5
shortest_path, length = aco.run(start_node, end_node)
print(shortest_path)
path = [shortest_path[0][0]]
for spot in shortest_path:
    if spot[1] != spot[0]:
        path.append(spot[1])
if shortest_path is None:
    print("No path found from {} to {}.".format(start_node, end_node))
else:
    print("Shortest path: ", path)
    print("Length of the shortest path: ", length)
