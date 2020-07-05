#!/usr/bin/env python3
import csv
import sys
import math
import itertools
from make_distance_matrix import cal_dist
from common import print_tour, read_input
import numpy as np


def make_tour_greedy(dist, start_point):
    unvisited_cities = set(range(0, N))
    current_city = start_point
    # tour = [current_city]

    tour = np.array(current_city)

    unvisited_cities.remove(current_city)

    while unvisited_cities:
        next_city = min(unvisited_cities, key=lambda city: dist[current_city][city])
        unvisited_cities.remove(next_city)
        # tour.append(next_city)
        tour = np.append(tour, next_city)
        # print(tour, next_city)
        current_city = next_city

    return tour



def save_file(path, tour): #結果保存
    with open(path, "w") as f:
     
        writer = csv.writer(f)
        writer.writerow(["index"])
        for city1_index in tour:
            writer.writerow([str(city1_index)])



def find_min_y_city(cities):
    min_y = 10**9
    min_y_city = -1
    for i in range(N):
        if cities[i][1] < min_y:
            min_y = cities[i][1]
            min_y_city = i

    return min_y_city



def cal_radian(dist, from_position_index, to_position_index):
    from_position = cities[from_position_index]
    to_position = cities[to_position_index]
    from_x = from_position[0]
    from_y = from_position[1]
    to_x = to_position[0]
    to_y = to_position[1]

    bec_x = to_x - from_x
    bec_y = to_y - from_y

    tan = math.atan2(bec_y, bec_x) #-pi から piまでで返ってくる

    return math.degrees(tan) #角度で返す



def make_outer_convex(dist, cities):
    unvisited_cities = [i for i in range(0, N)] 
    start_point = find_min_y_city(cities) #y座標が一番小さい都市から始める
   
    outer_tour = np.array(start_point)
    unvisited_cities.remove(start_point)

    from_position = start_point
    prev_radian = 200

    for _ in range(N):
        best_radian = -200
        best_index = None

        for to_position in range(N):
           
            if not to_position in outer_tour:
                radian = cal_radian(dist, from_position, to_position)
                if best_radian < radian and radian <= prev_radian: #最も角度が大きくなる都市を選ぶ

                    best_radian = radian
                    best_index = to_position
                    
        if best_index == None: #一周した
            break

        else:
            outer_tour = np.append(outer_tour, best_index)

            unvisited_cities.remove(best_index) 
            prev_radian = best_radian
            from_position = best_index

    return outer_tour, unvisited_cities



def cal_cost(dist, from_city_index, to_city_index, unvisited_city_index):
    cost = dist[from_city_index][unvisited_city_index] + dist[unvisited_city_index][to_city_index] - dist[from_city_index][to_city_index]
    return cost



def gift_packing(tour, dist, cities, unvisited_cities):
    while len(unvisited_cities) != 0:
        best_min_cost = 10**9 #全体の中で、最もコストが低い（次に訪問する）都市へのコスト
        next_city_candidate = None
        next_city_candidate_insert_position = None

        for unvisited_city_index in unvisited_cities: #全てのunvisited citiesについて最小の挿入コストを計算
            min_cost = 10**9
            min_cost_city_insert_position = None
   
            for i in range(len(tour) - 1):
                from_city_index = tour[i]
                to_city_index = tour[i + 1]

                cost = cal_cost(dist, from_city_index, to_city_index, unvisited_city_index)

                if min_cost > cost:
                    min_cost = cost #unvisited_city_indexを挿入するのにかかる最小コスト
                    min_cost_city_insert_position = i + 1 #unvisited_cityを挿入するとしたら、to_city_indexのところ

            if best_min_cost > min_cost:
                best_min_cost = min_cost
                next_city_candidate = unvisited_city_index
                next_city_candidate_insert_position = min_cost_city_insert_position 

        if next_city_candidate != None:
            tour = np.insert(tour, next_city_candidate_insert_position, next_city_candidate)
            unvisited_cities.remove(next_city_candidate)

    return tour



def cal_n_cities_dis(tour):
    sum_dis = 0
    for i in range(len(tour) - 1):
        sum_dis += dist[tour[i]][tour[i + 1]]

    return sum_dis



def cal_changed_dis(original_dis, splited_tour, inserted_tour): #入れ替えた後の距離を計算
    sum_dis = original_dis - dist[splited_tour[0]][splited_tour[1]] + dist[splited_tour[0]][inserted_tour[0]] + dist[splited_tour[1]][inserted_tour[-1]]

    return sum_dis



def check_dis_m_n(splited_tour, inserted_tour):
    original_dis = cal_n_cities_dis(splited_tour) + cal_n_cities_dis(inserted_tour)
    new_dis = cal_changed_dis(original_dis, splited_tour, inserted_tour)

    return original_dis > new_dis



def change_tour_m_n(tour, i, begin_city_index, end_city_index, inserted_tour): #end_city_index < begin_tour_indexになることもあるので注意
   
    original_tour = tour.copy()

    if begin_city_index < end_city_index: #0を跨がない

        if i < begin_city_index:
            tour = np.concatenate([original_tour[:i+1], inserted_tour]) #inserted_tourを抜いたtour
            tour = np.concatenate([tour, original_tour[i+1:begin_city_index]]) #inserted_tourが始まる前までを追加
            tour = np.concatenate([tour, original_tour[end_city_index:]]) #inserted_tourが終わった後から最後までを追加

        
        elif i >= end_city_index:
            tour = np.concatenate([original_tour[:begin_city_index], original_tour[end_city_index:i+1]]) #inserted_tourをのぞいて、インデックスiまでのtourを作る
            tour = np.concatenate([tour, inserted_tour]) #inserted_tourを追加
            tour = np.concatenate([tour, original_tour[i+1:]]) #インデックスi以降の都市を追加


    else: #0を跨ぐ
        tour = np.concatenate([original_tour[end_city_index:i+1], inserted_tour])
        tour = np.concatenate([tour, original_tour[i+1:begin_city_index]])

    assert(len(tour) == N)
    return tour



def get_min_tour_m_n(tour, count, splited_tour, inserted_tour, i, begin_city_index, end_city_index):
    if check_dis_m_n(splited_tour, inserted_tour): #m_citiesの0番目の都市をn_citiesの0番目に、m_citiesのm番目の都市をn_citiesのn番目につなぎ変える
        tour = change_tour_m_n(tour, i, begin_city_index, end_city_index, inserted_tour) #begin_city_index: inserted_tourの最初のインデックス, end_city_index: inserted_tourの最後のインデックス+1
                                                                          #i: splited_tourの最初のインデックス
        count += 1

    return tour, count



def make_split_tour(i, tour):
    if (i+2)%N < i: #0を跨ぐ
        splited_tour = np.concatenate([tour[i:], tour[:(i+2)%N ]])
    
    else:
        splited_tour = tour[i:(i+2)%N]

    return splited_tour



def m_n_opt(tour, n):
    
    while(True):
        count = 0
        for i in range(N):
            splited_tour = make_split_tour(i, tour)

            assert(len(splited_tour) == 2)

            for j in range((i+1)%N, (i+1)%N + N - n):
                begin_city_index = j%N
                end_city_index = (j+n)%N

                if end_city_index < begin_city_index: #0番目のcityを跨ぐ
                    inserted_tour = tour[begin_city_index:]
                    inserted_tour = np.concatenate([inserted_tour, tour[:end_city_index]], axis = 0)
                else:
                    inserted_tour = tour[begin_city_index: end_city_index]

                assert(len(inserted_tour) == n)
                tour, count = get_min_tour_m_n(tour.copy(), count, splited_tour, inserted_tour, i, begin_city_index, end_city_index)
            
        if (count == 0):
            break
        print(count)
        if count >= 1000:
            break
    return tour
    


def get_min_tour(dist, cities):
  
    tour, unvisited_cities = make_outer_convex(dist, cities) #凸包を探す

    tour = gift_packing(tour, dist, cities, unvisited_cities)

    assert(len(tour) == N)

    tour = m_n_opt(tour, 3)
    print("m_n_3 done")

    return tour


   
if __name__ == '__main__':
    global N

    if (len(sys.argv) > 1):
        cities = read_input(sys.argv[1])

        cities = np.array(cities)

        dist = cal_dist(cities) #データ読み込み
        N = len(dist)
        print("load done")

        tour = get_min_tour(dist, cities)

        tour = np.concatenate([tour, [tour[0]]]) #一周させる
        print(tour)

        dis = cal_n_cities_dis(tour)
        print(dis)

        print(sys.argv[1][6])
        path = "output_" + sys.argv[1][6] + ".csv"
        save_file(path, tour)

    else:
        for i in range(7):
            file_name = "input_" + str(i) + ".csv"
            cities = read_input(file_name)

            cities = np.array(cities)
            dist = cal_dist(cities) #データ読み込み
            N = len(dist)

            print("load done")

            tour = get_min_tour(dist, cities)

            tour += [tour[0]] #一周させる

            print("input_" + str(i))

            dis = cal_n_cities_dis(tour)
            print(dis)

            # print(sys.argv[1][6])
            # path = "output_" + sys.argv[1][6] + ".csv"
            # save_file(path, tour)







   