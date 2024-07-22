from math import sqrt
import operator

#1.构建用户-->物品的倒排
def loadData(files):
    data ={}
    for line in files:
        user,score,item=line.split(",")
        data.setdefault(user,{})
        data[user][item]=float(score)
    print(data)
    return data

def loadData2(files):
    data={}
    for line in files:
        user,item,score,timestamp=line.split(",")
        data.setdefault(user,{})
        data[user][item]=score
    return data

#2.计算
#2.1 构造物品-->物品的共现矩阵
#2.2 计算物品与物品的相似矩阵
#(这里采用的是余弦相似度算法计算的物品间的相似度)
def similarity(data):
    # 2.1 构造物品：物品的共现矩阵
    N={}#喜欢物品i的总人数
    C={}#喜欢物品i也喜欢物品j的人数
    for user,item in data.items():#遍历每个人的评分
        for i,score in item.items():#遍历每个景点的评分
            N.setdefault(i,0)
            N[i]+=1
            C.setdefault(i,{})
            for j,scores in item.items():
                if j != i:
                    C[i].setdefault(j,0)
                    C[i][j]+=1
    print(N)

    #2.2 计算物品与物品的相似矩阵
    W={}
    for i,item in C.items():
        W.setdefault(i,{})
        for j,item2 in item.items():
            W[i].setdefault(j,0)
            W[i][j]=C[i][j]/sqrt(N[i]*N[j])
            
    print("---3.构造的相似矩阵---")
    print(W)
    return W

#3.根据用户的历史记录，给用户推荐物品
def recommandList(data,W,user):
    rank={}
    for i,score in data[user].items():	#获得用户user历史记录，如A用户的历史记录为{'a': '1', 'b': '1', 'd': '1'}
        for j,w in sorted(W[i].items(),key=operator.itemgetter(1),reverse=True):	#获得与物品i相似的k个物品
            if j not in data[user].keys():	#该相似的物品不在用户user的记录里
                rank.setdefault(j,0)
                print(w)
                rank[j]+=float(score) * w
                
    results=sorted(rank.items(),key=operator.itemgetter(1),reverse=True)
    max_num,min_num=max(rank.values()),min(rank.values())
    final_results=[(i[0],(i[1]-min_num)/(max_num-min_num)) for i in results]

    print(dict(final_results))
    return dict(final_results)

if __name__=='__main__':
    # 用户，兴趣度，物品
    # 实例1
    uid_score_bid = ['A,4,1','A,3,3', 'A,4,5', 'A,5,6', 'B,5,2', 'B,4,3', 'C,5,1', 'C,4,2', 'C,2,3', 'D,2,1', 'D,4,2', 'D,3,4',
                     'E,3,1', 'E,5,3', 'E,4,2']
    data=loadData(uid_score_bid)	#获得数据
    W=similarity(data)	#计算物品相似矩阵
    recommandList(data,W,'C')	#推荐