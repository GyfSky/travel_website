import numpy as np
from flasker.routing_pkg.routing import *
'''
可选择起点和终点，但不包含用户兴趣的蚁群规划算法
'''

class AntColonyOptimizer:
    def __init__(self, distances, n_ants, n_best, n_iterations, decay, alpha=1, beta=1):
        self.distances = distances
        self.pheromone = np.ones(self.distances.shape) / len(distances)
        self.all_inds = range(len(distances))
        self.n_ants = n_ants
        self.n_best = n_best
        self.n_iterations = n_iterations
        self.decay = decay
        self.alpha = alpha
        self.beta = beta

    def run(self, start, end):
        shortest_path = None
        best_length = float('inf')
        for _ in range(self.n_iterations):
            all_paths = self.gen_all_paths(start, end)
            self.spread_pheromone(all_paths, self.n_best)
            shortest_path, best_length = self.find_best_path(all_paths, best_length, shortest_path)
            self.pheromone *= self.decay  # Decay pheromone
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
        heuristic = 1.0 / np.where(self.distances[current] > 0, self.distances[current], 1e-10)
        row = pheromone ** self.alpha * (heuristic ** self.beta)

        # Avoid division by zero or NaN by adding a small constant epsilon
        row_sum = row.sum() if row.sum() > 0 else 1e-10
        norm_row = row / row_sum

        if np.any(np.isnan(norm_row)) or np.all(norm_row == 0):
            return None  # Handle the case when no valid next node is available

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


# # Example usage:
# max = np.inf
# distances = np.array([
#     [max, max, 10, max, 30, 100],
#     [max, max, 5, max, max, max],
#     [max, max, max, 50, max, max],
#     [max, max, max, max, max, 10],
#     [max, max, max, 20, max, 60],
#     [max, max, max, max, max, max],
# ])

adjacent_matrix = get_adjacent_matrix(133, 149)  # 获取邻接矩阵
adjacent_matrix = np.array(adjacent_matrix)

aco = AntColonyOptimizer(adjacent_matrix, n_ants=10, n_best=5, n_iterations=100, decay=0.95, alpha=1, beta=2)
start_node = 0
end_node = 9
shortest_path, length = aco.run(start_node, end_node)
if shortest_path is None:
    print("No path found from {} to {}.".format(start_node, end_node))
else:
    print("Shortest path: ", shortest_path)
    print("Length of the shortest path: ", length)
