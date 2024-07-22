import operator
from math import sqrt, pow
import pandas as pd
from flasker.database.database_link import get_all_table


# 1.构建用户-->物品的倒排
def loadData_item(files, n, name):
    data = {}
    for line in files:
        data.setdefault(line[1], {})
        for i in range(10, n):
            if line[i] != None:
                data[line[1]][name[i]] = float(line[i])
    return data


# 2.计算
# 2.1 构造物品-->物品的共现矩阵
# 2.2 计算物品与物品的相似矩阵
# (这里采用的是余弦相似度算法计算的物品间的相似度)
def similarity(data):
    # 2.1 构造物品：物品的共现矩阵
    N = {}  # 喜欢物品i的总人数
    C = {}  # 喜欢物品i也喜欢物品j的人数
    for user, item in data.items():
        for i, score in item.items():
            N.setdefault(i, 0)
            N[i] += 1
            C.setdefault(i, {})
            for j, scores in item.items():
                if j not in i:
                    C[i].setdefault(j, 0)
                    C[i][j] += 1

    # print("---2.构造的共现矩阵---")
    # print ('N:',N)
    # print ('C:',C)

    # 2.2 计算物品与物品的相似矩阵
    W = {}
    for i, item in C.items():
        W.setdefault(i, {})
        for j, item2 in item.items():
            W[i].setdefault(j, 0)
            W[i][j] = C[i][j] / sqrt(N[i] * N[j])

    # print("---3.构造的相似矩阵---")
    # print(W)
    return W


# 3.根据用户的历史记录，给用户推荐物品
def recommandList(data, W, user):
    rank = {}
    for i, score in data[user].items():  # 获得用户user历史记录，如A用户的历史记录为{'a': '1', 'b': '1', 'd': '1'}
        for j, w in sorted(W[i].items(), key=operator.itemgetter(1), reverse=True):  # 获得与物品i相似的k个物品
            if j not in data[user].keys():  # 该相似的物品不在用户user的记录里
                rank.setdefault(j, 0)
                rank[j] += float(score) * w

    results = sorted(rank.items(), key=operator.itemgetter(1), reverse=True)
    max_num, min_num = max(rank.values()), min(rank.values())
    # final_results=[(i[0],(i[1]-min_num)/(max_num-min_num)) for i in results]
    final_results = []
    for i in results:
        if max_num != min_num:
            final_results.append((i[0], (i[1] - min_num) / (max_num - min_num)))
        else:
            # 处理`max_num == min_num`的情况
            final_results.append((i[0], 1))  # 或者其他默认值

    # print(dict(final_results))
    return dict(final_results)


def item_based(files, n, name, user):
    data = loadData_item(files, n, name)
    W = similarity(data)
    results = recommandList(data, W, user)
    return results

def only_item_based(files,n,name,user):
    data=loadData_item(files,n,name)
    temp=data[user]
    userdata={}
    for key,value in temp.items():
        userdata[key]=0
    results=recommandList(data,similarity(data),user)
    final_results=sorted({**userdata, **results}.items(),key=operator.itemgetter(1),reverse=True)
    return dict(final_results)

def loadData_user(files, n, name, user):
    data = {}
    data_pl = {}
    data_na = {}
    origin = []
    for i in range(10, n):
        data_pl.setdefault(name[i], 0)
        data_pl[name[i]] = str(i)
        data_na.setdefault(str(i), 0)
        data_na[str(i)] = name[i]
    for line in files:
        data.setdefault(line[1], {})
        for i in range(10, n):
            if line[i] != None:
                if user == line[1]:
                    origin.append(name[i])
                data[line[1]][data_pl[name[i]]] = float(line[i])
    return data, data_na, origin


class UserCf():

    # 获得初始化数据,计算每个用户的评分的平均值
    def __init__(self,data,name):
        temp=data.copy()
        self.data=data
        self.name=name
        self.ave = {}
        self.max = 0
        for key,value in temp.items():
            sum1 = 0.0
            for item,score in value.items():
                if(int(item)>self.max):
                    self.max = int(item)
                sum1 += score
            if len(temp[key])==0:
                del self.data[key]
                continue
            else:
                self.ave[key] = sum1/len(data[key])


        # 1.获取用户待预测分数的相关用户，如找到用户C中待评分商品4的预测分数相关用户A，D

    def find_user(self, item_goal):
        user_goal = []
        for key, values in self.data.items():
            for key1, value1 in values.items():
                if (key1 == item_goal):
                    user_goal.append(key)
                    break
        return user_goal

    # 2.计算待预测分数中相关用户中两个用户之间的皮尔逊相关系数
    def pearson(self, user1, item_goal):  # 数据格式为：商品，评分  A:{'a': 4.0, 'c': 3.0, 'd': 5.0
        user_goal = self.find_user(item_goal)
        denominator1 = 0.0  # 分母1--待预测用户的分母1
        denominator2 = 0.0  # 分母2--相关用户的分母2
        molecule = 0.0  # 分子
        r = {}  # 皮尔逊系数字典
        try:
            for user2 in user_goal:
                for item_, score_ in self.data[user2].items():
                    for item1, score1 in self.data[user1].items():
                        if (item_ == item1):
                            molecule += (float(score_) - self.ave[user2]) * (float(score1) - self.ave[user1])
                            denominator1 += pow(float(score1) - self.ave[user1], 2)
                            denominator2 += pow(float(score_) - self.ave[user2], 2)
                r.setdefault(user1, {})
                r[user1].setdefault(user2, 0)
                if denominator1 == 0 or denominator2 == 0:
                    r[user1][user2] = 0  # 或者设定其他默认值
                else:
                    r[user1][user2] = (molecule) / sqrt(denominator1 * denominator2)
                # r[user1][user2] = (molecule)/sqrt(denominator1*denominator2)
                molecule = 0.0
                denominator1 = 0.0
                denominator2 = 0.0
        except Exception as e:
            print("异常信息:", e)
            return None
        return r  # 返回相关用户的皮尔逊系数

    # 3.根据皮尔逊系数预测评分
    def prediction(self, user1, item_goal):
        ave1 = self.ave[user1]
        r = self.pearson(user1, item_goal)
        user_goal = self.find_user(item_goal)
        anw1 = 0.0
        anw2 = 0.0
        for user in user_goal:
            anw1 += r[user1][user] * ((self.data[user][item_goal]) - (self.ave[user]))
            anw2 += abs(r[user1][user])
        # predict = ave1 + anw1/anw2
        if anw2 != 0:
            predict = ave1 + anw1 / anw2
        else:
            # 当 anw2 是零时处理这种情况。
            # 你可以返回一个默认值或抛出异常。
            predict = ave1  # 或者选择其他你认为合适的默认值。
        self.data[user1][item_goal] = round(predict, 2)

    # 扫描数据集，收集未填充数据
    def scan(self):
        item_map = [str(i) for i in range(10, self.max + 1)]
        for user, value in self.data.items():
            item_list = []
            for m, n in value.items():
                item_list.append(m)
            for item in item_map:
                if (item not in item_list):
                    self.prediction(user, item)
        for user, value in self.data.items():
            self.data[user] = sorted(self.data[user].items(), key=lambda d: d[0])
        df = pd.DataFrame()

        for key, value in self.data.items():
            self.data[key] = dict(self.data[key])
            max_num = max(value, key=operator.itemgetter(1))[1]
            min_num = min(value, key=operator.itemgetter(1))[1]
            final_results = []
            for i in value:
                if max_num != min_num:
                    final_results.append((i[0], (i[1] - min_num) / (max_num - min_num)))
                else:
                    # 处理`max_num == min_num`的情况
                    final_results.append((i[0], 1))  # 或者其他默认值

            # value= [(i[0],(i[1]-min_num)/(max_num-min_num)) for i in value]
            df[key] = pd.Series(dict(final_results))
        return df[self.name]


def user_based(files, n, name1, user):
    data, data_na, origin = loadData_user(files, n, name1, user)
    userCf = UserCf(data=data, name=user)
    result = userCf.scan()
    final_result = {}
    for i in range(10, n):
        final_result[data_na[str(i)]] = float(result[i - 10])
    for i in origin:
        final_result[i] = 0
    return final_result


def fina_recommendation_(item_res, user_res):
    final_result = {}
    for key, value in user_res.items():
        final_result[key] = (item_res.get(key) if item_res.get(key) else 0 + user_res[key]) / 2
    final_result = sorted(final_result.items(), key=operator.itemgetter(1), reverse=True)

    return dict(final_result)


def fina_recommendation(files, n, name1, user):
    item_res = item_based(files, n, name1, user)
    user_res = user_based(files, n, name1, user)
    final_result = {}
    for key, value in user_res.items():
        final_result[key] = (item_res.get(key) if item_res.get(key) else 0 + user_res[key]) / 2
    final_result = sorted(final_result.items(), key=operator.itemgetter(1), reverse=True)

    return dict(final_result)

def recom_fresh(POOL):
    db = POOL.connection()
    cursor = db.cursor()
    sql = "select id,recommendation from node"
    cursor.execute(sql)

    cursor.close()
    db.close()

    result = [i[0] for i in sorted(cursor.fetchall(), key=operator.itemgetter(1), reverse=True)]
    return result
def get_recommendation(name):
    results, headers = get_all_table('users')
    return fina_recommendation(results, len(headers), headers, name)
