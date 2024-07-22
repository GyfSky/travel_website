# 用景点id来代替景点
class Spot:
    def __init__(self, name, index, id, introduction, spot_type, price, score, people, is_open):
        # 景点名字（string),景点索引(int),景点介绍（string),景点图片(路径),景点类型（int),景点价格（int),景点评分（float),景点人数（int，为空),景点是否开放（bool),景点权重（float，为空)
        self.name = name
        self.index = index  # 景点索引（景点在景点列表中对应的索引，从1开始一次递增）
        self.id = id  # 景点唯一的id（不是从一开始，且不一定连续）
        self.introduction = introduction
        # self.image = image
        self.type = spot_type
        self.price = price
        self.score = score
        self.people = people
        self.is_open = is_open
        # self.weight = weight
