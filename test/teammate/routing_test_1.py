import heapq
import queue


# 定义节点类
class Node:
    def __init__(self, x, y, g, h, parent):
        self.x = x
        self.y = y
        self.g = g
        self.h = h
        self.parent = parent

    def __lt__(self, other):
        return self.g + self.h < other.g + other.h


# 定义启发函数
def heuristic(node, goal):
    return abs(node.x - goal.x) + abs(node.y - goal.y)


# 定义A*算法函数
def astar(start, goal, grid):
    # 初始化open列表和closed列表
    open_list = []
    closed_list = set()

    # 将起点加入open列表
    heapq.heappush(open_list, start)

    # 循环直到找到终点或open列表为空
    while open_list:
        # 从open列表中选择一个节点
        current = heapq.heappop(open_list)

        # 如果该节点是终点，则搜索结束
        if current.x == goal.x and current.y == goal.y:
            path = []
            while current.parent:
                path.append((current.x, current.y))
                current = current.parent
            path.append((current.x, current.y))
            return path[::-1]

        # 将该节点从open列表中删除，并将其加入closed列表
        closed_list.add((current.x, current.y))

        # 遍历该节点的所有邻居节点
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            x = current.x + dx
            y = current.y + dy

            # 如果邻居节点不在grid中，则跳过
            if x < 0 or x >= len(grid) or y < 0 or y >= len(grid[0]) or grid[x][y] == 1:
                continue

            # 如果邻居节点已经在closed列表中，则跳过
            if (x, y) in closed_list:
                continue

            # 计算邻居节点到终点的距离
            h = heuristic(Node(x, y, 0, 0, None), goal)

            # 计算邻居节点到起的距离
            g = current.g + 1

            # 如果邻居节点不在open列表中，则将其加入open列表，并记录其父节点和到起点的距离
            if (x, y) not in [(node.x, node.y) for node in open_list]:
                heapq.heappush(open_list, Node(x, y, g, h, current))

            # 如果邻居节点已经在open列表中，则比较其到起点的距离，如果新的距离更小，则更新其父节点和到起点的距离
            else:
                for node in open_list:
                    if node.x == x and node.y == y:
                        if g < node.g:
                            node.g = g
                            node.parent = current

    # 如果open列表为空，则搜索失败
    return None


# 定义迷宫
grid = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 0, 1, 1, 0, 1, 1, 0],
        [0, 1, 1, 0, 1, 1, 0, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 1, 0],
        [0, 1, 0, 1, 1, 1, 0, 1, 1, 0],
        [0, 0, 0, 0, 0, 1, 0, 1, 1, 0],
        [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 1, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

# 定义起点和终点
start = Node(1, 1, 0, 0, None)
goal = Node(8, 8, 0, 0, None)

# 使用A*算法寻找最短路径
path = astar(start, goal, grid)

# 打印最短路径
print(path)