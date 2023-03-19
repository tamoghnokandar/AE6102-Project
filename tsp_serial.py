from itertools import permutations
import random
import argparse
from time import perf_counter

MIN_EDGE_WEIGHT = 1
MAX_EDGE_WEIGHT = 10
INF = 1e9


def find_path_cost(matrix, temp):
    cost = 0
    for i in range(1, len(temp)):
        cost += matrix[temp[i]][temp[i-1]]
    return cost


def tsp_serial(matrix):
    N = len(matrix[0])
    vertices = [i for i in range(1, N)]
    optimal_value = INF
    next_permutation = permutations(vertices)
    for i in next_permutation:
        temp = list(i)
        temp.append(0)
        temp.insert(0, 0)
        val = find_path_cost(matrix, temp)
        if val < optimal_value:
            optimal_value = val
            ans = temp
    return ans


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-N", default=4, type=int)
    args = parser.parse_args()
    N = args.N
    matrix = [[0 for _ in range(N)] for _ in range(N)]
    for i in range(N):
        for j in range(i+1, N):
            matrix[i][j] = random.randint(MIN_EDGE_WEIGHT, MAX_EDGE_WEIGHT)
            matrix[j][i] = matrix[i][j]
        matrix[i][i] = 0
    t1_start = perf_counter()
    tsp_serial(matrix)
    t1_stop = perf_counter()
    print("Time taken for {} cities is: {}".format(N, t1_stop-t1_start))
