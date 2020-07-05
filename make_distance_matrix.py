import numpy as np
import math

def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)



def init_dist(cities):
    dist = np.empty((N, N))
    for city1_index in range(N):
        for j in range(city1_index, N):
            dist[city1_index][j] = dist[j][city1_index] = distance(cities[city1_index], cities[j])

    return dist


def cal_dist(cities): #距離の隣接行列を作成
    global N
    N = len(cities)

    dist = init_dist(cities)

    return dist