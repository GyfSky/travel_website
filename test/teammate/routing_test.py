#!/bin/python
# -*- coding:utf-8 -*-
import numpy as np


def dijkstra(graph, startIndex, path, cost, max):
    """
    求解各节点最短路径，获取path，和cost数组，
    path[i] 表示vi节点的前继节点索引，一直追溯到起点。
    cost[i] 表示vi节点的花费
    """
    lenth = len(graph)
    v = [0] * lenth
    # 初始化 path，cost，V
    for i in range(lenth):
        if i == startIndex:
            v[startIndex] = 1
        else:
            cost[i] = graph[startIndex][i]
            path[i] = (startIndex if (cost[i] < max) else -1)
    # print v, cost, path
    for i in range(1, lenth):
        minCost = max
        curNode = -1
        for w in range(lenth):
            if v[w] == 0 and cost[w] < minCost:
                minCost = cost[w]
                curNode = w
        # for 获取最小权值的节点
        if curNode == -1: break
        # 剩下都是不可通行的节点，跳出循环
        v[curNode] = 1
        for w in range(lenth):
            if v[w] == 0 and (graph[curNode][w] + cost[curNode] < cost[w]):
                cost[w] = graph[curNode][w] + cost[curNode]  # 更新权值
                path[w] = curNode  # 更新路径
        # for 更新其他节点的权值（距离）和路径
    return path



if __name__ == '__main__':
    max = float('inf')
    graph = [
        [max, max, 10, max, 30, 100],
        [max, max, 5, max, max, max],
        [max, max, max, 50, max, max],
        [max, max, max, max, max, 10],
        [max, max, max, 20, max, 60],
        [max, max, max, max, max, max],
    ]


    path = [0] * 6
    cost = [0] * 6
    start_index = 1
    end_index = temp_end_index = 5
    path_index = [end_index]
    print(dijkstra(graph, start_index, path, cost, max))

    while path[temp_end_index]!=start_index:
        path_index.append(path[temp_end_index])
        temp_end_index = path[temp_end_index]
    path_index.append(start_index)
    path_index.reverse()
    if path_index.count(-1)>0:
        print(max)
    else:
        print("经过点顺序："+str(path_index))
        print(cost)


    # while path[temp_end_index] != start_index:
    #     path_index.append(path[temp_end_index])
    #     temp_end_index = path[temp_end_index]
    # path_index.append(end_index)
    # print(path_index)
    # print(cost)

