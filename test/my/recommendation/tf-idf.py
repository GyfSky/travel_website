# 1.引入依赖
import numpy as np
import pandas as pd

# 2.定义数据和预处理
spotA = "nature modern history history"
spotB = "nature nature history"

p1='nature nature nature modern'
p2='history history nature'


bowA = spotA.split(" ")
bowB = spotB.split(" ")

# 3.构建词库
wordSet = set(bowA).union(set(bowB))
wordSet # {'The', 'bed', 'cat', 'dog', 'knees', 'my', 'on', 'sat'}


# 进行词数统计
# 用统计字典来保存词出现的次数
wordDictA = dict.fromkeys(wordSet, 0)
wordDictB = dict.fromkeys(wordSet, 0)

# {'The': 0,
# 'sat': 0,
# 'cat': 0,
# 'on': 0,
# 'dog': 0,
# 'my': 0,
# 'bed': 0,
# 'knees': 0}

# 遍历文档，统计词数
for word in bowA:
    wordDictA[word] += 1
for word in bowB:
    wordDictB[word] += 1
    
#	The	sat	cat	on	dog	my	bed	knees
# 0	1	1	1	1	0	1	1	0
# 1	1	1	0	1	1	1	0	1

# 4.计算词频TF
def computeTF( wordDict, bow ):
    # 用一个字典对象记录tf，把所有的词对应在bow文档里的tf都算出来
    tfDict = {}
    nbowCount = len(bow)
    
    for word, count in wordDict.items():
        tfDict[word] = count / nbowCount
    return tfDict

tfA = computeTF(wordDictA, bowA)
tfB = computeTF(wordDictB, bowB)
tfA

# {'The': 0.16666666666666666,
# 'sat': 0.16666666666666666,
# 'cat': 0.16666666666666666,
# 'on': 0.16666666666666666,
# 'dog': 0.0,
# 'my': 0.16666666666666666,
# 'bed': 0.16666666666666666,
# 'knees': 0.0}

# 5.计算逆文档频率IDF
def computeIDF(wordDictList):
    # 用一个字典对象保存idf结果，每个词作为key，初始值为0
    idfDict = dict.fromkeys(wordDictList[0], 0)
    N = len(wordDictList)
    import math
    print(N)
    for wordDict in wordDictList:
        # 遍历字典中的每个词汇
        for word, count in wordDict.items():
            if count > 0:
                # 先把Ni增加1，存入到idfDict
                idfDict[word] += 1
    # print(idfDict)#算ni，即每个词在总文档中的出现次数
    # 已经得到所有词汇i对应的Ni，现在根据公式把它替换成为idf值
    for word, ni in idfDict.items():
        idfDict[word] = math.log10((N + 1) / (ni + 1))
    return idfDict

idfs = computeIDF([wordDictA, wordDictB])
idfs

# {'The': 0.0,
# 'sat': 0.0,
# 'cat': 0.17609125905568124,
# 'on': 0.0,
# 'dog': 0.17609125905568124,
# 'my': 0.0,
# 'bed': 0.17609125905568124,
# 'knees': 0.17609125905568124}

# 6.计算TF-IDF
def computeTFIDF(tf, idfs):
    tfidf = {}
    for word, tfval in tf.items():
        tfidf[word] = tfval * idfs[word]
    return tfidf

tfidfA = computeTFIDF(tfA, idfs)
tfidfB = computeTFIDF(tfB, idfs)

pd.DataFrame([tfidfA, tfidfB])
print(pd.DataFrame([tfidfA, tfidfB]))
# 	The	sat	cat			on	dog			my	bed			knees
# 0	0.0	0.0	0.029349	0.0	0.000000	0.0	0.029349	0.000000
# 1	0.0	0.0	0.000000	0.0	0.029349	0.0	0.000000	0.029349
