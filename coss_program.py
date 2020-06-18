#!/usr/bin/env python3
import csv
import sys
import math
import itertools

from common import print_tour, read_input

def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)



def cal_path_length(dist, tour):
    path_length = sum(dist[tour[i]][tour[(i + 1) % N]] for i in range(N))
    return path_length



def init_dist():
    dist = [[0] * N for city1_index in range(N)]
    for city1_index in range(N):
        for j in range(city1_index, N):
            dist[city1_index][j] = dist[j][city1_index] = distance(cities[city1_index], cities[j])

    return dist



def make_tour_greedy(dist, start_point):
    unvisited_cities = set(range(0, N))
    current_city = start_point
    tour = [current_city]
    unvisited_cities.remove(current_city)

    while unvisited_cities:
        next_city = min(unvisited_cities,
                        key=lambda city: dist[current_city][city])
        unvisited_cities.remove(next_city)
        tour.append(next_city)
        current_city = next_city

    return tour



def cal_dist(cities):
    global N
    N = len(cities)

    dist = init_dist()

    return dist



def check_min_way_three(tour, city1_index, city2_index, city3_index, city4_index, city5_index):
    dis1_2 = dist[tour[city1_index]][tour[city2_index]]
    dis2_3 = dist[tour[city2_index]][tour[city3_index]]
    dis4_5 = dist[tour[city4_index]][tour[city5_index]]
    dis1_3 = dist[tour[city1_index]][tour[city3_index]]
    dis2_4 = dist[tour[city2_index]][tour[city4_index]]
    dis2_5 = dist[tour[city2_index]][tour[city5_index]]

    if dis1_2 + dis2_3 + dis4_5 > dis1_3 + dis2_4 + dis2_5:
        return True #変えた方が短くなる
    else:
        return False



def chenge_tour_three(tour, i, j):
    poped = tour.pop(i) #抜き出す要素
    
    if i < j:
        tour.insert(j, poped) #iがポップされたことにより、jの位置が前より一個後ろの要素(city5) を指していることに注意
    else:
        tour.insert(j + 1, poped)

    return tour



def three_opt(N, tour):
    p = 0
    while(p < 20):
        count = 0

        for i in range(N):
            city1_index = i - 1
            city2_index = i
            city3_index = (i + 1) % N

            for j in range((i + 2) % N, (i + 2) % N + N - 4):
                city4_index = j % N
                city5_index = (j + 1) % N

                if check_min_way_three(tour, city1_index, city2_index, city3_index, city4_index, city5_index):
                    tour = chenge_tour_three(tour, city2_index, city4_index)
                    count += 1
                    
        if count == 0:
            break
        p += 1
  
    if p == 20: #無限ループの可能性あり、強制終了
        print("break")
        exit()
    return tour



def check_min_way_two(tour, city1_index, city2_index, city3_index, city4_index):
    dist1_2 = dist[tour[city1_index]][tour[city2_index]]
    dist3_4 = dist[tour[city3_index]][tour[city4_index]]
    dist1_3 = dist[tour[city1_index]][tour[city3_index]]
    dist2_4 = dist[tour[city2_index]][tour[city4_index]]

    if (dist1_2 + dist3_4 > dist1_3 + dist2_4):
        return True #変えた方が短くなる
    else:
        return False


def chenge_tour_two(tour, city2_index, city4_index):

    new_path = tour[city2_index:city4_index] 
    tour[city2_index:city4_index] = new_path[::-1]

    return tour



def opt_2(N, tour):
    global dist

    p = 0
    while (True):
        count = 0
        for i in range(N - 2):
            city1_index = i
            city2_index = i + 1

            for j in range(i + 2, N):
                city3_index = j
                city4_index = (j + 1) % N

                if city1_index != 0 or city4_index != 0:
                    if check_min_way_two(tour, city1_index, city2_index, city3_index, city4_index):
                        tour = chenge_tour_two(tour, city2_index, city3_index + 1)
                        count += 1

        if count == 0: break

        p += 1
        if p >= 20:
            print("break")
            exit()

    return tour



def save_file(path, tour):
    with open(path, "w") as f:
     
        writer = csv.writer(f)
        writer.writerow(["index"])
        for city1_index in tour:
            writer.writerow([str(city1_index)])

if __name__ == '__main__':

    assert len(sys.argv) > 1
    cities = read_input(sys.argv[1])
    dist = cal_dist(cities) #データ読み込んでやるときはこっち
    
    print("load done")
    min_distance = 10**9

    for start_point in range(N):
        tour = make_tour_greedy(dist, start_point)

        
        tour = three_opt(N, tour)
        # print("three done")

        tour = opt_2(N, tour)
        # print("two done")

        path_length = cal_path_length(dist, tour)
        if min_distance > path_length:
            min_distance = path_length
            min_tour = tour
            print(min_distance)

    # print(tour)
    # print(sys.argv[1][6])
    # path = "output_" + sys.argv[1][6] + ".csv"
    # save_file(path, tour)

   