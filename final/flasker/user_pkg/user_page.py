from flasker.user_pkg.UserClass import *
from flasker.database.database_link import *
from flasker.spot_pkg.spot_msg import *


# 创建用户对象，获得用户的所有属性
def user(username, password):
    msg = get_user_msg(username)
    user_name = User(*msg)
    return user_name


# 选择路线
def user_route(username, consume, interest, score, start_spot, end_spot=None):
    # 距离最短路线
    pass
    # 推荐观光路线
    pass
    # 消费+兴趣+评分+推荐景点


# 用户增加景点
def user_addspot(username, spot_name):
    # 获得景点标签
    spot_name = spot(spot_name)
    add_spotIndex = spot_name.index
    # 处理邻接矩阵
    return add_spotIndex


# 用户取消景点
def user_deletespot(username, spot_name):
    # 获得景点标签
    spot_name = spot(spot_name)
    delete_spotIndex = spot_name.index
    # 处理邻接矩阵
    return delete_spotIndex

# 景点打分
def user_spotscore(username, score):
    user_name = user(username, "")
    user_name.score = score
    # update_user_score(username, score)


# 路线打分
def user_routescore(username, score):
    user_name = user(username, "")
    user_name.score = score
    # update_user_score(username, score)


