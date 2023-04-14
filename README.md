# AE6102 Course Project
## Parallel Implementation of Travelling Salesman Problem
***

- Week 1 Update: Serial code for TSP `tsp_serial.py` was implemented. Run this file using the command ``python tsp_serial.py -N <Number of Cities>``. Note that number of cities is an unsigned integer.
- Week 2 Update: Parallelized serial code(converted to C++ version) using CUDA. Original plan was to use Numba+CUDA but there are some errors which are taking time to resolve. Will try to complete that by next week. `tsp_cuda.cu` was implemented.
- Week 3 Update: Parallelized serial code(Python version) using mPI4Py Library. `tsp_serial.py` was implemented.
