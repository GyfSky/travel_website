import numpy as np

from flasker.database.database_link import *
from flasker.routing_pkg.routing_algorithm import *
from flasker.routing_pkg.routing import *
from flasker.spot_pkg.spot_msg import *


# print()
# a = get_distance(133, 134)[0][0]
# print(type(a))
# print(a)
# print('-'*100)

# # 测试Dijkstra算法
# adjacent_matrix = get_adjacent_matrix()  # 获取邻接矩阵
# print(adjacent_matrix)
# start_index = 0
# end_index = temp_end_index = 15
#
# path = [0] * adjacent_matrix.shape[0]
# cost = [0] * adjacent_matrix.shape[0]
# print(adjacent_matrix.shape[0])
# path_index = [end_index]
# dijkstra(adjacent_matrix, start_index, path, cost, MAX)
# print(path)
# if path[end_index] == 0:  # 初始情况下，若路径未设置，这里可以判断为无路径
#     print("No path found")
# else:
#     while path[temp_end_index] != start_index:
#         if path[temp_end_index] == -1:  # 检查是否指向未设置的前驱节点
#             print("No valid path")
#             break
#         path_index.append(path[temp_end_index])
#         temp_end_index = path[temp_end_index]
#     else:
#         path_index.append(start_index)
#         path_index.reverse()
# if path_index.count(-1) > 0:
#     print(MAX)
# else:
#     print(path_index)  # 返回最短路线的索引

# # 测试蚁群算法
# adjacent_matrix = [
#     [max, max, 10, max, 30, 100],
#     [max, max, 5, max, max, max],
#     [max, max, max, 50, max, max],
#     [max, max, max, max, max, 10],
#     [max, max, max, 20, max, 60],
#     [max, max, max, max, max, max],
# ]
#
# adjacent_matrix = np.array(adjacent_matrix)
# print(ant_colony_optimization(adjacent_matrix))


# 测试用户添加和访问
# add_user('test2',12345)
# if is_existed('test1',12345):
#     print('用户已存在')
# else:
#     print('用户不存在')

# # 测试指定概率执行代码函数
# sum = 0
# for i in range(100):
#     if possible_runcode(0.8):
#         sum += 1
# print(sum)


# # 测试获取景点信息
# spot = spot(133)
# print(spot.name)
# print(spot.index)
# print(type(spot))
# print(spot)

# #
# print(get_distance(218,140))
#
# # 测试获得邻接矩阵
# adjacent_matrix = get_adjacent_matrix()
# print(adjacent_matrix)
# # 检测邻接矩阵中np.inf的个数
# inf_mask = np.isinf(adjacent_matrix)
# num_inf = np.sum(inf_mask)
# print(num_inf)


# path = recommend_route('users_1', 196, 135)
# print(path)
# path = get_path(path)
# print(path)


def select_route(username, start_spot_id, end_spot_id, consume=None, interest=None, score=None):
    start_index = get_index_by_id(start_spot_id)
    end_index = get_index_by_id(end_spot_id)
    path = allspots_ACO(adjacent_matrix, start_index, end_index)
    path = [get_id_by_index(i) for i in path]
    print('path',path)
    # 根据兴趣过滤
    if interest:
        interest_spots = set()
        for i in interest:
            spot_ids = get_spot_id_by_type(i)
            interest_spots.update(spot_ids)  # 将列表中的所有元素添加到集合中
        print('interest_spots:', interest_spots)
        path = list(set(path) & interest_spots)  # 取路径和兴趣点的交集
        if start_spot_id not in path:
            path.append(start_spot_id)  # 确保起点在路径中
        if end_spot_id not in path:
            path.append(end_spot_id)  # 确保终点在路径中
        print('经兴趣筛选后，剩余景点为：', path)
    # 根据评分过滤
    if score:
        try:
            min_score = min(score)
            max_score = max(score)
            path = [i for i in path if min_score < get_spot_score(i) <= max_score or i in [start_spot_id, end_spot_id]]
            path = list(dict.fromkeys(path))  # 删除重复元素
        except ValueError:
            print('请输入一个最大值和一个最小值的评分列表')
        print('经评分筛选后，剩余景点为：', path)
    if consume:
        try:
            min_consume = min(consume)
            max_consume = max(consume)
        except ValueError:
            print('请输入一个最大值和一个最小值的消费范围')
        optimal_path, optimal_score, optimal_cost = optimize_path(path, min_consume, max_consume)
        return optimal_path


if __name__ == '__main__':
    username = 'users_1'
    start_spot_id = 133
    end_spot_id = 133
    consume = [0, 50]
    interest = ["A", 'B', 'E', 'F']
    score = [3.2, 5.0]
    path = select_route(username, start_spot_id, end_spot_id, consume, interest, score)
    print('final path:', path)


# print(get_spot_id_by_type('A'))
#
# print(recommend_route('users_1', 133, 218))