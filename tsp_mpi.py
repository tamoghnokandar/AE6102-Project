from itertools import permutations
import random
from mpi4py import MPI


MIN_EDGE_WEIGHT = 1
MAX_EDGE_WEIGHT = 10
MAXN = 16
INF = 1e9

factorial = [0 for i in range(MAXN+1)]

"""
def fact(n):
  ans = 1
  for i in range(1,n+1):
    ans *= i
  return ans
"""

def precompute_factorial():
  factorial[0] = 1
  for i in range(1,MAXN+1):
    factorial[i] = i * factorial[i-1]

def assign_edge_weights(matrix, N):
  for i in range(N):
    for j in range(i+1, N):
        matrix[i][j] = random.randint(MIN_EDGE_WEIGHT, MAX_EDGE_WEIGHT)
        matrix[j][i] = matrix[i][j]
    matrix[i][i] = 0

def nth_permutation(arr, n):
  arrsize = len(arr)
  if(n>factorial[arrsize]):
    return arr
  taken = [False for i in range(arrsize)]
  ans = [0 for i in range(arrsize)]
  for i in range(arrsize):
    cn = 1
    cval = factorial[arrsize-1-i]
    while(cval<n):
      cn += 1
      cval=cn*cval
      cval=cval//(cn-1)
    pval = cval*(cn-1)//cn
    n -= pval
    for j in range(arrsize):
      if not taken[j]:
        cn -= 1
        if cn == 0:
          ans[i] = arr[j]
          taken[j] = True
          break
  for i in range(arrsize):
    arr[i] = ans[i]
  return arr

def nxt_permutation(arr, n):
  nxt_permutation_possible = False
  fi = -1
  for i in range(n-2,-1,-1):
    if(arr[i+1] > arr[i]):
      nxt_permutation_possible = True
      fi = i
      break
  if not nxt_permutation_possible:
    return arr
  next_greater_ele = arr[fi+1]
  next_greater_ele_ind = fi+1
  for i in range(fi+2,n):
    if(arr[i] > arr[fi] and arr[i] < next_greater_ele):
      next_greater_ele = arr[i]
      next_greater_ele_ind = i
  arr[fi], arr[next_greater_ele_ind] = arr[next_greater_ele_ind], arr[fi]
  li = fi+1
  ri = n-1
  while li<ri:
    arr[li], arr[ri] = arr[ri], arr[li]
    li += 1
    ri -= 1
  return arr


def find_path_cost(matrix, temp):
    cost = 0
    for i in range(1, len(temp)):
        cost += matrix[temp[i]][temp[i-1]]
    return cost

if __name__ == "__main__":
    #parser = argparse.ArgumentParser()
    #parser.add_argument("-N", default=4, type=int)
    #args = parser.parse_args()
    comm = MPI.COMM_WORLD
    size = comm.Get_size()
    rank = comm.Get_rank()
    precompute_factorial()
    N = 4
    ans = [0 for i in range(N+1)]
    matrix = [[0 for _ in range(N)] for _ in range(N)]
    if rank == 0:
      assign_edge_weights(matrix, N)
    if rank == 0:
      for pe in range(1,size):
        for i in range(0,N):
          comm.Send(matrix[i][0], des=pe, tag=pe)
    else:
      for i in range(0,N):
          comm.Recv(matrix[i][0], source=0, tag=rank)
    comm.Barrier()
    start = MPI.Wtime()
    optimal_value = INF
    nppe = factorial[N-1]/size
    rem = factorial[N-1]%size
    nodes = [i for i in range(1,N)]
    if rem == 0:
      start_perm_ind = (rank*nppe) + 1
      end_perm_ind = (rank + 1)*nppe
    else:
      if rank < rem:
        start_perm_ind = (rank*(nppe + 1)) + 1
        end_perm_ind = (rank + 1)*(nppe + 1)
		
      else:
        start_perm_ind = rem*(nppe + 1) + (rank - rem)*nppe + 1
        end_perm_ind = rem*(nppe + 1) + (rank + 1 - rem)*nppe
    if start_perm_ind <= end_perm_ind:
      nodes_begin = nth_permutation(nodes, start_perm_ind)
      nodes_end = nth_permutation(nodes, end_perm_ind)
      next_permutation = permutations(nodes_begin)
      for i in next_permutation:
        nodes_begin = list(i)
        temp = list(i)
        temp.append(0)
        temp.insert(0, 0)
        val = find_path_cost(matrix, temp)
        if val < optimal_value:
            optimal_value = val
            my_ans = temp
        if(nodes_begin == nodes_end):
            break
      ans = my_ans
    if rank == 0:
      for pe in range(1,size):
        tmp_optimal_value = 0
        tmp_ans = [0 for i in range(N+1)]
        comm.Recv(tmp_ans[0], source=pe, tag=pe)
        comm.Recv(tmp_optimal_value, source=pe, tag=pe)
        if tmp_optimal_value<optimal_value:
          optimal_value = tmp_optimal_value
          ans = tmp_ans
    else:
      comm.Send(ans[0], dest=0, tag=rank);
      comm.Send(optimal_value, dest=0, tag=rank)
    comm.Barrier()
    end = MPI.Wtime()
    if rank==0:
      print(end-start)
    MPI.Finalize()
