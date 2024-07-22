class User:
    def __init__(self, id, username, password, interest, min_consume, max_consume, min_distance, max_distance,
                 min_score, max_score):
        self.username = username
        self.password = password
        self.interest = interest
        self.min_consume = min_consume
        # interest:基于用户过去的浏览记录、搜索记录、已访问过的景点、对景点的评价和反馈等。
        self.max_consume = max_consume
        # consume:基于用户过去的消费记录、消费行为、消费偏好等。
        self.min_score = min_score
        self.max_score = max_score
        # score:基于用户过去的评分记录、评分行为、评分偏好等。
        self.min_distance = min_distance
        self.max_distance = max_distance
        self.se_id = id
        # distance:基于用户过去的距离记录、距离行为、距离偏好等。
