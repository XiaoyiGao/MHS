# -*- coding: utf-8 -*-
import os
import sys;sys.path.append('..')
from data import build_graph
from subgraph_txt import sub_jump,random_choice,random_jump,sub_jump_pro,sub_jump_n,top_degree

num_random_trials = 1000
p = 1                  # 在候选邻居中选择度数最大节点的概率
t = 0                  # 无思考随机选择的概率

# Define the parameter ranges
k_values = [1, 5, 10, 20]
n_values = [1, 2, 3, 4, 5]
b_values = [0, 0.2, 0.4, 0.6, 0.8, 1]

for a in range(1, 4):
    # 动态生成路径
    path = f'BA/BA_{a}/BA_{a}.txt'
    G = build_graph(path)
    print(G)

    for k in k_values:
        for n in n_values:
            for b in b_values:
                # 动态生成文件夹路径
                folder_base = fr'C:\Users\lenovo\Desktop\SSA_test\k_{k}_n_{n}_b_{b}\BA\BA_{a}'

                jump_steps = [1, 2, 3, 4]
                # 批量创建文件夹
                for step in jump_steps:
                    folder = os.path.join(folder_base, f'sub_jump_{step}')
                    os.makedirs(folder, exist_ok=True)

                    # 调用跳跃函数
                    sub_jump_n(G, num_random_trials, step, k, n, b, p, t, folder)