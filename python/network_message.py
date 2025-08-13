import networkx as nx

def read_graph_from_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    # 读取节点数和边数
    node_count, edge_count = map(int, lines[0].strip().split())

    G = nx.Graph()  # 创建无向图

    # 读取边的信息
    for line in lines[1:]:
        u, v = map(int, line.strip().split())
        G.add_edge(u, v)

    return G,node_count,edge_count


def read_graph(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    G = nx.Graph()  # 创建无向图

    # 读取边的信息并添加到图中
    for line in lines:
        u, v = map(int, line.strip().split(' '))  # 注意这里使用了逗号作为分隔符
        G.add_edge(u, v)

    # 获取图中的节点数和边数
    node_count = G.number_of_nodes()
    edge_count = G.number_of_edges()

    return G, node_count, edge_count


# 从指定的文件读取图
filename = 'graphs/a/email-enron-only.txt'
G,node,edge = read_graph(filename)


# 输出节点数和边数
print("节点数：", node)
print("边数：", edge)

