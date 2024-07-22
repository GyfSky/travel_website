from flasker.spot_pkg.spot_msg import *
from flasker.routing_pkg.routing import *
from flasker.database.database_link import *

'''
求出的所有景点的花费在范围内，且景点的评分尽量高
'''

def get_spot_info(spot_id):
    spot_ = spot(spot_id)
    return spot_.price, spot_.score if spot_ else (0, 0)


def optimize_path(path, min_consume, max_consume):
    n = len(path)
    dp = [[-1] * (max_consume + 1) for _ in range(n + 1)]
    dp[0][0] = 0

    for i in range(1, n + 1):
        price, score = get_spot_info(path[i - 1])
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
            price, score = get_spot_info(path[i - 1])
            cost -= price

    return result_path[::-1], best_score, best_cost


# 示例路径和消费范围
path = [60, 59, 55, 56, 57, 58, 50, 49, 28, 24, 22, 21, 13, 17, 16, 7, 2]

print('path:', path)
print('path length:', len(path))
min_consume = 0
max_consume = 10

path = [get_id_by_index(i) for i in path]
optimal_path, optimal_score, optimal_cost = optimize_path(path, min_consume, max_consume)

print(f"Optimal Path: {optimal_path}")
print(f"Path length: {len(optimal_path)}")
print(f"Optimal Score: {optimal_score}")
print(f"Optimal Cost: {optimal_cost}")
