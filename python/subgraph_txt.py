# -*- coding: utf-8 -*-
import random
import networkx as nx


def sub_1(G, num_random_trials, step, n, output_dir):
    total_percentage = 0  # 用于累加所有循环中的子图占比
    for trial in range(num_random_trials):
        #print(f"子图1的第{trial + 1}次循环")

        # 创建一个空图
        G_sub = nx.Graph()
        initial_node = random.choice(list(G.nodes()))
        selected_nodes = {initial_node}

        # 复制一个局部的 step 来避免影响其他试验
        current_step = step

        while current_step > 0:  # 只要还有步数，就继续扩展
            # 打印当前步骤
            #print(f"第{step - current_step + 1}步")
            neighbors = [neighbor for neighbor in G.neighbors(initial_node) if neighbor not in selected_nodes]

            if not neighbors:  # 如果当前节点没有未访问的邻节点
                # 将当前节点添加到子图中
                G_sub.add_node(initial_node)
                current_step -= 1
                #print(f"将当前节点 {initial_node} 添加到子图，并减少步数。剩余步数：{current_step}")

                while True:
                    # 查询未访问的节点
                    unvisited_nodes = [node for node in G.nodes() if node not in selected_nodes]
                    if not unvisited_nodes:  # 如果没有未访问的节点，退出循环
                        #print("没有未访问的节点，结束扩展。")
                        break

                    # 从未访问的节点中随机选择一个节点
                    initial_node = random.choice(unvisited_nodes)
                    # 再次检查新选择的节点是否有邻节点
                    neighbors = [neighbor for neighbor in G.neighbors(initial_node) if neighbor not in selected_nodes]
                    if neighbors:  # 找到有邻节点的节点，跳出循环
                        #print(f"找到的邻节点有：{neighbors}")
                        break
                    else:
                        break

            if neighbors:  # 如果找到有邻节点的节点
                #print(f"找到的邻节点有：{neighbors}")
                # 获取度数最高的前 n 个邻节点
                #top_neighbors = sorted(neighbors, key=lambda n: G.degree(n), reverse=True)[:n]
                top_neighbors = random.sample(neighbors, min(n, len(neighbors)))
                #print(f"选择的邻节点有：{top_neighbors}")
                # 将度数最大的前 n 个邻节点添加到子图 G_sub 中
                for neighbor in top_neighbors:
                    if neighbor != initial_node:
                        G_sub.add_node(neighbor)
                        G_sub.add_edge(initial_node, neighbor)

                # 选择度数最高的邻节点作为下一个初始节点
                initial_node = top_neighbors[0]

            # 标记当前节点为已访问
            selected_nodes.add(initial_node)

            # 每一轮都减1步
            current_step -= 1

        #print(f"节点数：{G_sub.number_of_nodes()}")
        # 输出子图到txt文件，并添加随机数列
        # 输出子图到txt文件，并添加随机数列
        output_file = f"{output_dir}/subgraph_1_{trial + 1}.txt"
        with open(output_file, "w") as f:
            # 写入第一行：节点数 空格 边数
            f.write(f"{G_sub.number_of_nodes()} {G_sub.number_of_edges()}\n")

            # 输出每一条边及其随机值
            for edge in G_sub.edges():
                random_value = round(random.uniform(0.1, 0.9), 1)  # 生成0.1到0.9之间的随机数，并保留两位小数
                f.write(f"{edge[0]} {edge[1]} {random_value}\n")

        #print(f"第{trial+1}次循环的子图已保存到 {output_file}")
        # 计算子图占比并累加
        subgraph_percentage = 100 * G_sub.number_of_nodes() / G.number_of_nodes()
        total_percentage += subgraph_percentage
    # 输出所有循环的平均子图占比
    average_percentage = total_percentage / num_random_trials
    print(f"子图1的平均子图占比：{average_percentage:.2f}%")

def sub_2(G, num_random_trials, step, n, output_dir):
    total_percentage = 0
    for trial in range(num_random_trials):
        #print(f"子图2的第{trial+1}次循环")
        G_sub = nx.Graph()
        initial_nodes = random.sample(list(G.nodes()), step // 2)  # 随机选择 step // 2 个初始节点
        selected_nodes = set(initial_nodes)  # 记录已访问节点

        # 对每个初始节点，找到其度数最大的前10个邻接点并添加到子图中
        for initial_node in initial_nodes:
            G_sub.add_node(initial_node)
            if G.neighbors(initial_node):
                # 按度数排序选择前10个度数最大的邻接点
                top_neighbors = sorted(G.neighbors(initial_node), key=lambda n: G.degree(n), reverse=True)[:n]
                #top_neighbors = random.sample(list(G.neighbors(initial_node)),min(n, len(list(G.neighbors(initial_node)))))

                for neighbor in top_neighbors:
                    G_sub.add_node(neighbor)
                    G_sub.add_edge(initial_node, neighbor)
                next_node = None
                for neighbor in top_neighbors:
                    if neighbor not in selected_nodes:  # 确认选择为访问的邻接点
                        next_node = neighbor
                        break
                if next_node:
                    selected_nodes.add(next_node)
                    top_neighbors = sorted(G.neighbors(next_node), key=lambda n: G.degree(n), reverse=True)[:n]
                    #top_neighbors = random.sample(list(G.neighbors(next_node)),min(n, len(list(G.neighbors(next_node)))))

                    for neighbor in top_neighbors:
                        if neighbor not in selected_nodes:
                            G_sub.add_node(neighbor)
                            G_sub.add_edge(next_node, neighbor)
        #print(f"节点数：{G_sub.number_of_nodes()}")
        # 输出子图到txt文件，并添加随机数列
        # 输出子图到txt文件，并添加随机数列
        output_file = f"{output_dir}/subgraph_2_{trial + 1}.txt"
        with open(output_file, "w") as f:
            # 写入第一行：节点数 空格 边数
            f.write(f"{G_sub.number_of_nodes()} {G_sub.number_of_edges()}\n")

            # 输出每一条边及其随机值
            for edge in G_sub.edges():
                random_value = round(random.uniform(0.1, 0.9), 1)  # 生成0.1到0.9之间的随机数，并保留两位小数
                f.write(f"{edge[0]} {edge[1]} {random_value}\n")

        #print(f"第{trial+1}次循环的子图2已保存到 {output_file}")
        # 计算子图占比并累加
        subgraph_percentage = 100 * G_sub.number_of_nodes() / G.number_of_nodes()
        total_percentage += subgraph_percentage
    # 输出所有循环的平均子图占比
    average_percentage = total_percentage / num_random_trials
    print(f"子图2的平均子图占比：{average_percentage:.2f}%")

def random_1(G, num_random_trials, step, n, output_dir):
    total_percentage = 0
    for trial in range(num_random_trials):
        #print(f"随机子图的第{trial+1}次循环")
        random_sub = nx.Graph()

        selected_nodes = set(random.sample(list(G.nodes()), step))

        # 对每个选中的节点，随机选择 1 到 n 个邻居
        for node in selected_nodes:
            # 获取该节点的所有邻居
            neighbors = list(G.neighbors(node))

            # 随机选择 1 到 n 个邻居，确保选择的邻居数量不超过可用邻居数
            num_neighbors = random.randint(1, min(n, len(neighbors)))

            # 随机从邻居中选择 num_neighbors 个
            selected_neighbors = random.sample(neighbors, num_neighbors)

            # 将当前节点和选择的邻居添加到子图中
            random_sub.add_node(node)
            for neighbor in selected_neighbors:
                random_sub.add_node(neighbor)
                random_sub.add_edge(node, neighbor)
        #print(f"节点数：{random_sub.number_of_nodes()}")

        # 输出子图到txt文件，并添加随机数列
        output_file = f"{output_dir}/random_{trial + 1}.txt"
        with open(output_file, "w") as f:
            # 写入第一行：节点数 空格 边数
            f.write(f"{random_sub.number_of_nodes()} {random_sub.number_of_edges()}\n")

            # 输出每一条边及其随机值
            for edge in random_sub.edges():
                random_value = round(random.uniform(0.1, 0.9), 1)  # 生成0.1到0.9之间的随机数，并保留两位小数
                f.write(f"{edge[0]} {edge[1]} {random_value}\n")

        #print(f"第{trial+1}次循环的随机子图已保存到 {output_file}")
        # 计算子图占比并累加
        subgraph_percentage = 100 * random_sub.number_of_nodes() / G.number_of_nodes()
        total_percentage += subgraph_percentage
    # 输出所有循环的平均子图占比
    average_percentage = total_percentage / num_random_trials
    print(f"随即图的平均子图占比：{average_percentage:.2f}%")

def sub_3(G, num_random_trials, step, n, output_dir):
    total_percentage = 0
    for trial in range(num_random_trials):
        #print(f"子图3的第{trial+1}次循环")
        G_sub = nx.Graph()
        initial_nodes = random.sample(list(G.nodes()), step // 5)  # 随机选择 step // 5 个初始节点
        selected_nodes = set(initial_nodes)  # 记录已访问节点

        # 对每个初始节点，找到其度数最大的前10个邻接点并添加到子图中
        for initial_node in initial_nodes:
            current_node = initial_node
            G_sub.add_node(current_node)  # 添加到子图中
            previous_top_neighbors = []  # 记录上一轮的邻接点
            for _ in range(5):
                # 获取初始节点的所有邻接点
                neighbors = list(G.neighbors(current_node))

                # 选择度数最大的前n个邻接点
                top_neighbors = sorted(neighbors, key=lambda n: G.degree(n), reverse=True)[:n]
                # 将邻接点和边添加到子图中
                G_sub.add_nodes_from(top_neighbors)
                G_sub.add_edges_from([(current_node, neighbor) for neighbor in top_neighbors])

                # 找到度数最大的未被选择的邻接点作为下一个节点
                next_node = None
                for neighbor in top_neighbors:
                    if neighbor not in selected_nodes:
                        next_node = neighbor
                        break
                if not next_node and previous_top_neighbors:
                    for neighbor in previous_top_neighbors:
                        if neighbor not in selected_nodes:
                            next_node = neighbor
                            break
                current_node = next_node if next_node else current_node
                selected_nodes.add(current_node)
                previous_top_neighbors = top_neighbors

        # 输出子图到txt文件，并添加随机数列
        output_file = f"{output_dir}/subgraph_3_{trial+1}.txt"
        with open(output_file, "w") as f:
            # 输出每一条边及其随机值
            for edge in G_sub.edges():
                random_value = round(random.uniform(0.1, 0.9), 1)  # 生成0.1到0.9之间的随机数，并保留两位小数
                f.write(f"{edge[0]} {edge[1]} {random_value}\n")

        #print(f"第{trial+1}次循环的子图3已保存到 {output_file}")
        # 计算子图占比并累加
        subgraph_percentage = 100 * G_sub.number_of_nodes() / G.number_of_nodes()
        total_percentage += subgraph_percentage
    # 输出所有循环的平均子图占比
    average_percentage = total_percentage / num_random_trials
    print(f"子图3的平均子图占比：{average_percentage:.2f}%")

def sub_jump(G, num_random_trials, m, k, output_dir):
    for trial in range(num_random_trials):
        #print(f'子图的第{trial+1}次循环')

        # 随机选择 k 个初始节点
        selected_nodes = set(random.sample(list(G.nodes()), k))
        #print(f'初始选择的节点：{selected_nodes}')

        # 对每个节点进行 m 步跳跃
        final_nodes = set()  # 用于存储每个节点的 m 步跳跃后的最终目标节点

        for node in selected_nodes:
            #print(f"处理节点{node}")
            current_node = node  # 当前节点
            for _ in range(m):
                neighbors = [neighbor for neighbor in G.neighbors(current_node) if neighbor not in final_nodes]
                #print(f"邻接点有：{neighbors}")
                if neighbors:
                    # 选择度数最大的邻居节点作为下一个目标
                    top_neighbor = max(neighbors, key=lambda n: G.degree(n))
                    current_node = top_neighbor  # 更新为下一个目标节点
                    #print(f'新访问节点：{current_node}')
                else:
                    # 如果没有邻居节点可以跳跃，提前结束
                    break

            # 最终跳跃后的目标节点加入 final_nodes 集合
            final_nodes.add(current_node)

        #print(f'最终选择的节点集合：{final_nodes}')
        # 这里可以输出最终的 final_nodes 到文件
        output_file = f"{output_dir}/jump_{m}_{trial + 1}.txt"
        with open(output_file, "w") as f:
            # 输出每个最终节点
            for node in final_nodes:
                f.write(f"{node}\n")

import os

def top_degree(G, k, output_dir):
    """
    选择度数最大的 k 个节点，并将结果保存到一个文件中。

    参数：
    - G: 网络图
    - k: 选择的节点数（种子节点数）
    - output_dir: 输出文件路径
    """
    os.makedirs(output_dir, exist_ok=True)  # 确保输出目录存在

    # ✅ 提取度数最大的 k 个节点
    top_k_nodes = [node for node, _ in sorted(G.degree, key=lambda x: x[1], reverse=True)[:k]]

    # ✅ 生成输出文件路径
    output_file = os.path.join(output_dir, "top_degree_nodes.txt")

    # ✅ 将节点写入文件
    with open(output_file, "w") as f:
        for node in top_k_nodes:
            f.write(f"{node}\n")  # ✅ 只写入节点编号

    print(f"度数最大的 {k} 个节点已保存到 {output_file}")


def sub_jump_n(G, num_random_trials, m, k, n, p1, p2, p3, output_dir):
    """
    多次随机跳跃实验，结合多概率参数。

    参数：
    - G: 网络图
    - num_random_trials: 随机实验次数
    - m: 跳跃步数
    - k: 初始种子节点数
    - n: 每次推选的邻居数量
    - p1: 概率1 -> 是否随机或认真推选邻居
    - p2: 概率2 -> 在候选中选择度数最大的节点或随机选择
    - p3: 概率3 -> 是否进行无思考随机选择
    - output_dir: 输出文件路径
    """

    os.makedirs(output_dir, exist_ok=True)  # 确保输出目录存在

    for trial in range(num_random_trials):
        # ✅ 随机选择 k 个初始种子节点
        selected_nodes = set(random.sample(list(G.nodes()), k))

        # ✅ 存储最终跳跃到的节点集合
        final_nodes = set()

        for node in selected_nodes:
            current_node = node  # 当前访问节点

            for _ in range(m):
                neighbors = list(G.neighbors(current_node))

                if not neighbors:
                    break  # 无邻居，结束跳跃

                # ✅ 概率 p3：无思考随机选择
                if random.random() < p3:
                    candidates = random.sample(neighbors, min(n, len(neighbors)))
                    current_node = random.choice(candidates)
                    continue

                # ✅ 概率 p1：随机推选或认真推选
                if random.random() < p1:
                    # 随机推选N个邻居
                    candidates = random.sample(neighbors, min(n, len(neighbors)))
                else:
                    # 认真推选：轮盘赌法选择
                    total_degree = sum(G.degree(nb) for nb in neighbors)
                    probabilities = [G.degree(nb) / total_degree for nb in neighbors]
                    candidates = random.choices(neighbors, probabilities, k=min(n, len(neighbors)))

                # ✅ 概率 p2：在候选邻居中选择度数最大 or 随机选择
                if random.random() < p2:
                    next_node = max(candidates, key=lambda x: G.degree(x))
                else:
                    next_node = random.choice(candidates)

                current_node = next_node

            # 将最终跳跃后的节点加入集合
            final_nodes.add(current_node)

        # ✅ 将最终节点集合输出到文件
        output_file = f"{output_dir}/jump_{m}_{trial + 1}.txt"
        with open(output_file, "w") as f:
            for node in final_nodes:
                f.write(f"{node}\n")

    print(f"所有实验结果已保存到 {output_dir}")


def sub_jump_score(G, num_random_trials, m, k, n, p1, p2, p3, output_dir):
    """
    多次随机跳跃实验，结合多概率参数和评分机制。

    参数：
    - G: 网络图
    - num_random_trials: 随机实验次数
    - m: 跳跃步数
    - k: 初始种子节点数
    - n: 每次推选的邻居数量
    - p1: 概率1 -> 是否随机或认真推选邻居
    - p2: 概率2 -> 在候选中选择度数最大的节点或随机选择
    - p3: 概率3 -> 是否进行无思考随机选择
    - output_dir: 输出文件路径
    """

    os.makedirs(output_dir, exist_ok=True)  # 确保输出目录存在

    for trial in range(num_random_trials):
        # ✅ 随机选择 k 个初始种子节点
        selected_nodes = set(random.sample(list(G.nodes()), k))

        # ✅ 初始化评分字典
        node_scores = {node: 0 for node in G.nodes()}

        for node in selected_nodes:
            current_node = node  # 当前访问节点

            for _ in range(m):
                neighbors = list(G.neighbors(current_node))

                if not neighbors:
                    break  # 无邻居，结束跳跃

                # ✅ 概率 p3：无思考随机选择
                if random.random() < p3:
                    candidates = random.sample(neighbors, min(n, len(neighbors)))
                    # 给被推荐的候选节点加分
                    for candidate in candidates:
                        node_scores[candidate] += 1
                    current_node = random.choice(candidates)
                    continue

                # ✅ 概率 p1：随机推选或认真推选
                if random.random() < p1:
                    # 随机推选N个邻居
                    candidates = random.sample(neighbors, min(n, len(neighbors)))
                else:
                    # 认真推选：轮盘赌法选择
                    total_degree = sum(G.degree(nb) for nb in neighbors)
                    probabilities = [G.degree(nb) / total_degree for nb in neighbors]
                    candidates = random.choices(neighbors, probabilities, k=min(n, len(neighbors)))

                # 给被推荐的候选节点加分
                for candidate in candidates:
                    node_scores[candidate] += 1

                # ✅ 概率 p2：在候选邻居中选择度数最大 or 随机选择
                if random.random() < p2:
                    next_node = max(candidates, key=lambda x: G.degree(x))
                else:
                    next_node = random.choice(candidates)

                current_node = next_node

        # ✅ 获取得分最高的前k个节点
        sorted_nodes = sorted(node_scores.items(), key=lambda x: x[1], reverse=True)
        top_k_nodes = [node for node, score in sorted_nodes[:k]]

        # ✅ 将最终节点集合输出到文件
        output_file = f"{output_dir}/jump_{m}_{trial + 1}.txt"
        with open(output_file, "w") as f:
            for node in top_k_nodes:
                f.write(f"{node}\n")

    print(f"所有实验结果已保存到 {output_dir}")

def sub_jump_pro(G, num_random_trials, m, k, output_dir, p):
    """
    带概率选择度数最大的邻居节点的跳跃算法

    参数：
    - G: 网络图
    - num_random_trials: 实验次数
    - m: 每个节点跳跃的步数
    - k: 初始种子节点数
    - output_dir: 输出文件目录
    - p: 选择度数最大邻居的概率，范围 (0, 1]
    """
    os.makedirs(output_dir, exist_ok=True)  # 确保输出目录存在

    for trial in range(num_random_trials):
        # 随机选择 k 个初始节点
        selected_nodes = set(random.sample(list(G.nodes()), k))

        # 存储最终跳跃节点
        final_nodes = set()

        for node in selected_nodes:
            current_node = node  # 当前节点
            for _ in range(m):
                neighbors = list(G.neighbors(current_node))

                if not neighbors:
                    # 如果当前节点没有邻居，结束跳跃
                    break

                if random.random() < p:
                    # 以 p 概率选择度数最大的邻居
                    next_node = max(neighbors, key=lambda n: G.degree(n))
                else:
                    # 以 (1-p) 概率随机选择邻居
                    next_node = random.choice(neighbors)

                current_node = next_node

            final_nodes.add(current_node)

        # 将最终跳跃的节点写入文件
        output_file = f"{output_dir}/jump_{m}_{trial + 1}.txt"
        with open(output_file, "w") as f:
            for node in final_nodes:
                f.write(f"{node}\n")

        print(f"实验 {trial + 1}/{num_random_trials} 完成，结果保存至：{output_file}")


def sub_jump_a(G, num_random_trials, m, k, l, output_dir):      #从k中随机选择l个节点
    # 检查 l 是否小于等于 k
    if l > k:
        raise ValueError("l 必须小于或等于 k")

    for trial in range(num_random_trials):
        #print(f'子图的第{trial+1}次循环')

        # 随机选择 k 个初始节点
        selected_nodes = set(random.sample(list(G.nodes()), k))
        #print(f'初始选择的节点：{selected_nodes}')

        # 对每个节点进行 m 步跳跃
        final_nodes = set()  # 用于存储每个节点的 m 步跳跃后的最终目标节点

        for node in selected_nodes:
            #print(f"处理节点{node}")
            current_node = node  # 当前节点
            for _ in range(m):
                neighbors = [neighbor for neighbor in G.neighbors(current_node) if neighbor not in final_nodes]
                #print(f"邻接点有：{neighbors}")
                if neighbors:
                    # 选择度数最大的邻居节点作为下一个目标
                    top_neighbor = max(neighbors, key=lambda n: G.degree(n))
                    current_node = top_neighbor  # 更新为下一个目标节点
                    #print(f'新访问节点：{current_node}')
                else:
                    # 如果没有邻居节点可以跳跃，提前结束
                    break

            # 最终跳跃后的目标节点加入 final_nodes 集合
            final_nodes.add(current_node)

        # 从 final_nodes 中随机选择 l 个节点
        if len(final_nodes) > l:
            final_nodes = set(random.sample(list(final_nodes), l))

        #print(f'最终选择的节点集合：{final_nodes}')
        # 输出最终的 final_nodes 到文件
        output_file = f"{output_dir}/jump_{m}_{trial + 1}.txt"
        with open(output_file, "w") as f:
            # 输出每个最终节点
            for node in final_nodes:
                f.write(f"{node}\n")

def random_jump(G, num_random_trials, m, k, n, output_dir):
    for trial in range(num_random_trials):
        selected_nodes = set(random.sample(list(G.nodes()), k))
        node_scores = {node: 0 for node in G.nodes()}

        # 对每个选中的节点，随机选择 1 到 n 个邻居
        for node in selected_nodes:
            current_node = node  # 当前节点
            for _ in range(m):
                # 获取当前节点的所有邻居
                neighbors = list(G.neighbors(current_node))
                if neighbors:
                    # 随机选择 1 到 n 个邻居，确保选择的邻居数量不超过可用邻居数
                    num_neighbors = random.randint(1, min(len(neighbors), n))  # 例如随机选择 1 到 n 个邻居
                    selected_neighbors = random.sample(neighbors, num_neighbors)

                    # 将选中的邻居的分数加 1
                    for neighbor in selected_neighbors:
                        node_scores[neighbor] += 1

                    # 从选中的邻居中随机选择一个作为下一轮的访问节点
                    current_node = random.choice(selected_neighbors)
                else:
                    # 如果没有邻居节点可以跳跃，提前结束
                    break

                # 按照节点分数降序排序，选出前 k 个节点
        top_k_nodes = sorted(node_scores.items(), key=lambda item: item[1], reverse=True)[:k]
        top_k_nodes = [node for node, score in top_k_nodes]


        #print(f'最终选择的节点集合：{final_nodes}')
        # 这里可以输出最终的 final_nodes 到文件
        output_file = f"{output_dir}/random_jump_{m}_{trial + 1}.txt"
        with open(output_file, "w") as f:
            # 输出每个最终节点
            for node in top_k_nodes:
                f.write(f"{node}\n")

def random_choice(G, num_random_trials, k, output_dir):
    for trial in range(num_random_trials):
        selected_nodes = set(random.sample(list(G.nodes()), k))
        output_file = f"{output_dir}/random_{k}_{trial + 1}.txt"
        with open(output_file, "w") as f:
            for node in selected_nodes:
                f.write(f"{node}\n")

def random_neighbor(G, num_random_trials, k, output_dir):
    for trial in range(num_random_trials):
        selected_nodes = set(random.sample(list(G.nodes()), k))
        for node in selected_nodes:
            neighbors = list(G.neighbors(node))
            if neighbors:
                key_nodes = random.choice(neighbors)
        output_file = f'{output_dir}/rn_{k}_{trial + 1}.txt'
        with open(output_file, 'w') as f:
            for node in key_nodes:
                f.write(f"{node}\n")

def random_edge(G, num_random_trials, k, output_dir):
    for trial in range(num_random_trials):
        selected_edges = random.sample(list(G.edges()), k)
        key_nodes = []
        for edge in selected_edges:
            selected_node = random.choice(edge)
            key_nodes.append(selected_node)
        output_file = f'{output_dir}/re_{k}_{trial + 1}.txt'
        with open(output_file, 'w') as f:
            for node in key_nodes:
                f.write(f"{node}\n")

















