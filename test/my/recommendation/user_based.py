from math import sqrt,pow
import operator
import pandas as pd

class UserCf():

    #获得初始化数据,计算每个用户的评分的平均值
    def __init__(self,data,name):
        self.data=data
        self.name=name
        self.ave = {}
        self.max = 0
        for key,value in self.data.items():
            sum1 = 0.0
            for item,score in value.items():
                if(int(item)>self.max):
                    self.max = int(item)
                sum1 += score
            self.ave[key] = sum1/len(data[key])
        print(self.ave)

        #1.获取用户待预测分数的相关用户，如找到用户C中待评分商品4的预测分数相关用户A，D
    def find_user(self,item_goal):
        user_goal = []
        for key,values in self.data.items():
            for key1,value1 in values.items():
                if(key1 == item_goal):
                    user_goal.append(key)
                    break
        return user_goal

    #2.计算待预测分数中相关用户中两个用户之间的皮尔逊相关系数
    def pearson(self,user1,item_goal):#数据格式为：商品，评分  A:{'a': 4.0, 'c': 3.0, 'd': 5.0
        user_goal = self.find_user(item_goal)
        denominator1 = 0.0 #分母1--待预测用户的分母1
        denominator2 = 0.0 #分母2--相关用户的分母2
        molecule = 0.0     #分子
        r = {}             #皮尔逊系数字典
        try:
            for user2 in user_goal:
                for item_, score_ in self.data[user2].items():
                    for item1,score1 in self.data[user1].items():
                        if(item_ == item1):
                            molecule += (float(score_)-self.ave[user2])*(float(score1)-self.ave[user1])
                            denominator1 += pow(float(score1)-self.ave[user1],2)
                            denominator2 += pow(float(score_)-self.ave[user2],2)
                r.setdefault(user1, {})
                r[user1].setdefault(user2,0)
                r[user1][user2] = (molecule)/sqrt(denominator1*denominator2)
                molecule = 0.0
                denominator1 = 0.0
                denominator2 = 0.0
        except Exception as e:
            print("异常信息:",e)
            return None
        return r#返回相关用户的皮尔逊系数

    #3.根据皮尔逊系数预测评分
    def prediction(self,user1, item_goal):
        ave1 = self.ave[user1]
        r = self.pearson(user1,item_goal)
        user_goal = self.find_user(item_goal)
        anw1 = 0.0
        anw2 = 0.0
        for user in user_goal:
            anw1 += r[user1][user]*((self.data[user][item_goal])-(self.ave[user]))
            anw2 += abs(r[user1][user])
        predict = ave1 + anw1/anw2
        self.data[user1][item_goal] = round(predict,2)

    #扫描数据集，收集未填充数据
    def scan(self):
        item_map = [str(i) for i in range(2,self.max+1)]
        for user,value in self.data.items():
            item_list = []
            for m,n in value.items():
                item_list.append(m)
            for item in item_map:
                if(item not in item_list):
                    self.prediction(user,item)
        for user, value in self.data.items():
            self.data[user] = sorted(self.data[user].items(),key = lambda d:d[0])

        df=pd.DataFrame()

        for key,value in self.data.items():
            self.data[key] = dict(self.data[key])
            max_num=max(value,key=operator.itemgetter(1))[1]
            min_num=min(value,key=operator.itemgetter(1))[1]
            value= [(i[0],(i[1]-min_num)/(max_num-min_num)) for i in value]
            df[key]=pd.Series(dict(value))
        return df[self.name]

if __name__=='__main__':
    users = {'A': {'2': 4.0, '3': 3.0,'5': 4.0,'6': 4.0},
             'B': {'2': 5.0, '3': 4.0},
             'C': {'4': 5.0, '2': 4.0,'3': 2.0},
             'D': {'3': 2.0, '2': 4.0,'4': 3.0},
             'E': {'4': 3.0, '2': 4.0,'3': 5.0},
             }
    userCf=UserCf(data=users,name='A')
    # recommandList=userCf.scan()
    # print(recommandList)

