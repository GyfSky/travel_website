from flasker.spot_pkg.SpotClass import *
from flasker.database.database_link import get_adjacent_matrix
from flasker.routing_pkg.routing_algorithm import *
from flasker.spot_pkg.spot_msg import *
import numpy as np


MAX = np.inf



# 以某一概率执行某段代码
def possible_runcode(odds):
    r = random.random()
    return True if odds > r else False


# 距离最短路线(Dijkstra算法)
# （应用场景:历程最短，用户选定起点和终点）
def shortest_path(start_id, end_id,POOL):
    start_index = get_index_by_id(start_id)  # 起始景点的索引
    adjacent_matrix = get_adjacent_matrix()
    end_index = temp_end_index = get_index_by_id(end_id)  # 终止景点的索引
    path = [0] * adjacent_matrix.shape[0]
    cost = [0] * adjacent_matrix.shape[0]
    print(path)
    print(cost)
    path_index = [end_index]
    dijkstra(adjacent_matrix, start_index, path, cost, MAX)
    if path[end_index] == 0:  # 初始情况下，若路径未设置，这里可以判断为无路径
        print("No path found")
    else:
        while path[temp_end_index] != start_index:
            if path[temp_end_index] == -1:  # 检查是否指向未设置的前驱节点
                print("No valid path")
                break
            path_index.append(path[temp_end_index])
            temp_end_index = path[temp_end_index]
        else:
            path_index.append(start_index)
            path_index.reverse()
    if path_index.count(-1) > 0:
        return MAX
    else:
        return path_index  # 返回最短路线的索引


# 推荐观光路线（根据游客评分、兴趣偏好得到的景点推荐权重，直接生成推荐路线）
# （应用场景：老用户什么也不选，直接点开始规划，但必须选起点和终点）
def recommend_route(start_id, end_id,final_reco,POOL):
    # 获得用户的景点推荐
    # interests = get_recommendation(username)
    adjacent_matrix = get_adjacent_matrix(POOL)
    interests = final_reco
    print('interests:', interests)
    new_dict = {int(key.split('_')[-1]): value for key, value in interests.items()}
    interests = [0] * len(interests)

    for key, value in new_dict.items():
        spot_index = get_index_by_id(key,POOL)
        interests[spot_index] = value
    print('interests:', interests)
    interests = np.array(interests)
    start_index, end_index = get_index_by_id(start_id,POOL), get_index_by_id(end_id,POOL)
    path = ant_colony_optimization(adjacent_matrix, interests, start_index, end_index)
    path = [get_id_by_index(i,POOL) for i in path]
    return path


# 消费+兴趣+评分+推荐景点+用户旅游距离习惯(传入消费范围，兴趣列表，评分范围(最低分），筛选出一个满足所有条件的邻接矩阵，送入规划算法中)
# 先考虑兴趣，再考虑评分，再考虑消费
# 点有权重、边也有权重
# 将点权重与启发函数联系
def select_route(POOL,username, start_spot_id, end_spot_id,add_spot_ids,consume=None, interest=None, score=None):
    adjacent_matrix = get_adjacent_matrix(POOL)
    start_index = get_index_by_id(start_spot_id,POOL)
    end_index = get_index_by_id(end_spot_id,POOL)
    path = allspots_ACO(adjacent_matrix, start_index, end_index)
    path = [get_id_by_index(i,POOL) for i in path]
    print('path',path)
    # 根据兴趣过滤
    if interest:
        interest_spots = set()
        for i in interest:
            spot_ids = get_spot_id_by_type(i,POOL)
            interest_spots.update(spot_ids)  # 将列表中的所有元素添加到集合中
        print('interest_spots:', interest_spots)
        path = [i for i in path if
                i in interest_spots or i in [start_spot_id, end_spot_id] or i in add_spot_ids]  # 取路径和兴趣点的交集
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
            path = [i for i in path if min_score < get_spot_score(i,POOL) <= max_score or i in [start_spot_id,
                                                                                           end_spot_id] or i in add_spot_ids]
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
        path, optimal_score, optimal_cost = optimize_path(path, min_consume, max_consume,POOL)
        print('经消费筛选后，最终景点为：', path)
    return path


# 用户自定义路线(全部景点都是用户选择的，地图会自动生成一个最优的路径，无需算法）
def user_route(spots):
    path = [get_spot_name_by_id(i) for i in spots]
    return path


# 官方推荐路线（根据游客反馈的最优路线？）
# 花费最少路线
def waste_route():
    pass


# 路程最短
def shortest_route():
    pass


# 全景点游
def all_spots_route():
    pass


# 根据返回的路径id生成对应的中文路径
def get_path(path,POOL):
    path_ = []
    for i in path:
        path_.append(get_spot_name_by_id(i,POOL))
    return path_


#  求出的所有景点的花费在范围内，且景点的评分尽量高
def get_spot_info(spot_id,POOL):
    spot_ = spot(spot_id,POOL)
    return spot_.price, spot_.score if spot_ else (0, 0)


def optimize_path(path, min_consume, max_consume,POOL):
    n = len(path)
    dp = [[-1] * (max_consume + 1) for _ in range(n + 1)]
    dp[0][0] = 0

    for i in range(1, n + 1):
        price, score = get_spot_info(path[i - 1],POOL)
        for j in range(max_consume + 1):
            if dp[i - 1][j] != -1:
                dp[i][j] = max(dp[i][j], dp[i - 1][j])
                if j + price <= max_consume:
                    dp[i][j + price] = max(dp[i][j + price], dp[i - 1][j] + score)

    best_score = -1
    best_cost = 0
    for cost in range(min_consume, max_consume + 1):
        if dp[n][cost] > best_score:
            best_score = dp[n][cost]
            best_cost = cost

    result_path = []
    cost = best_cost
    for i in range(n, 0, -1):
        if cost >= 0 and dp[i][cost] != dp[i - 1][cost]:
            result_path.append(path[i - 1])
            price, score = get_spot_info(path[i - 1],POOL)
            cost -= price

    return result_path[::-1], best_score, best_cost
