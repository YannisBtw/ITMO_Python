# Результаты замеров

n_iter = 2000000

|   iteration | method       | detail              |   n_jobs |   n_iter |        sec |
|------------:|:-------------|:--------------------|---------:|---------:|-----------:|
|           1 | python       | baseline sin        |        1 |  2000000 | 0.0938391  |
|           2 | threads      | ThreadPoolExecutor  |        2 |  2000000 | 0.0951086  |
|           2 | threads      | ThreadPoolExecutor  |        4 |  2000000 | 0.0942634  |
|           2 | threads      | ThreadPoolExecutor  |        6 |  2000000 | 0.0950183  |
|           2 | threads      | ThreadPoolExecutor  |        8 |  2000000 | 0.0947595  |
|           3 | processes    | ProcessPoolExecutor |        2 |  2000000 | 0.403144   |
|           3 | processes    | ProcessPoolExecutor |        4 |  2000000 | 0.433724   |
|           3 | processes    | ProcessPoolExecutor |        6 |  2000000 | 0.468149   |
|           3 | processes    | ProcessPoolExecutor |        8 |  2000000 | 0.544832   |
|           4 | cython       | C-level sin         |        1 |  2000000 | 0.00847953 |
|           4 | cython       | loop + py-call sin  |        1 |  2000000 | 0.0535731  |
|           5 | cython_nogil | OpenMP prange sin   |        2 |  2000000 | 0.0083781  |
|           5 | cython_nogil | OpenMP prange sin   |        4 |  2000000 | 0.007756   |
|           5 | cython_nogil | OpenMP prange sin   |        6 |  2000000 | 0.00487367 |
