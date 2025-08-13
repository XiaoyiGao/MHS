# -*- coding: utf-8 -*-
import networkx as nx

def build_graph(file_path):
    """
    从 txt 文件读取网络图数据，不考虑边权重。

    参数：
    - file_path: txt文件路径，第一行是节点数和边数，后续是边（无权重）

    返回：
    - G: NetworkX 无向图
    """
    G = nx.Graph()  # 无向图

    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()

        # 读取节点数和边数
        node_count, edge_count = map(int, lines[0].split())
        print(f"加载图：节点数 = {node_count}, 边数 = {edge_count}")

        # 添加边（忽略权重）
        for line in lines[1:]:
            u, v, _ = line.split()  # 忽略权重
            u, v = int(u), int(v)
            G.add_edge(u, v)

    return G


def data_load(path):
    '''Load data from path
    Args: 
        path (str): path to data files;
    '''
    nodes = []
    edges = []
    file = open(path)
    for line in file:
        source, target = line.split(' ')
        nodes.append(int(source))
        nodes.append(int(target))
        edges.append((int(source), int(target)))
    nodes = list(set(nodes))
    num_nodes = len(nodes)
    num_edges = len(edges)
    print('Number of Nodes: {}'.format(num_nodes))
    print('Number of Edges: {}'.format(num_edges))
    return nodes, edges


def build_graph_from_txt(file_path):
    # 创建一个无向图
    G = nx.Graph()

    # 读取文件并添加边
    with open(file_path, 'r') as f:
        for line in f:
            # 每行数据是由空格或制表符分隔的节点对
            nodes = line.split()
            if len(nodes) == 2:
                # 添加一条无向边到图中
                G.add_edge(nodes[0], nodes[1])

    return G

def build_digraph_from_txt(file_path):
    # 创建一个有向图
    G = nx.DiGraph()

    # 读取文件并添加边
    with open(file_path, 'r') as f:
        # 第一行通常是节点数和边数，不需要处理（可以跳过）
        f.readline()
        for line in f:
            # 每行数据是由空格分隔的节点对和边权重
            nodes = line.split()
            if len(nodes) == 3:  # 确保有3个元素：节点1, 节点2, 权重
                node1, node2, weight = nodes
                weight = float(weight)  # 将权重转换为浮动类型
                G.add_edge(node1, node2, weight=weight)  # 添加有向边，并附带权重

    return G