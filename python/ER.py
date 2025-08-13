import networkx as nx
import numpy as np
import os
import random

# 参数设置
n = 10000                  # 节点数
p = 5 / (n - 1)            # 理论连接概率
num_graphs = 20             # 生成20个 ER 网络
base_output_dir = "./ER"    # 主输出文件夹

# 创建主输出文件夹（若不存在）
os.makedirs(base_output_dir, exist_ok=True)

# 批量生成 ER 网络
for i in range(1, num_graphs + 1):
    # 生成 ER 图
    G = nx.erdos_renyi_graph(n, p)

    # 将节点编号从 1 开始
    mapping = {node: node + 1 for node in G.nodes()}
    G = nx.relabel_nodes(G, mapping)

    # 随机为每条边赋权重（0.1 到 0.9，保留1位小数）
    edges_with_weights = [(u, v, round(random.uniform(0.1, 0.9), 1)) for u, v in G.edges()]

    # 创建单独的子文件夹
    sub_dir = os.path.join(base_output_dir, f"ER_{i}")
    os.makedirs(sub_dir, exist_ok=True)

    # 文件路径
    file_path = os.path.join(sub_dir, f"ER_{i}.txt")

    # 写入文件
    with open(file_path, "w") as f:
        # 写入第一行：节点数和边数
        f.write(f"{n} {len(G.edges())}\n")

        # 写入边信息：节点1 节点2 权重
        for u, v, weight in edges_with_weights:
            f.write(f"{u} {v} {weight}\n")

    # 显示生成状态
    print(f"✅ 文件 {file_path} 已生成 | 节点数: {n}, 边数: {len(G.edges())}")

print("\n🎯 所有 ER 网络生成完成！")
