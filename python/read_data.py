import pandas as pd
import os

# 基础路径
base_path = 'C://Users//Lenovo//Desktop//code//SSA_test//add//k//k_1//BA//'

def process_folder(folder_name):
    """
    处理单个文件夹中的数据
    :param folder_name: 文件夹名称，例如 'BA_1'
    :return: 处理后的 DataFrame
    """
    folder_path = os.path.join(base_path, folder_name)
    df_all = pd.DataFrame()

    # 读取 random_edge 的数据
    random_edge_dir = os.path.join(folder_path, 'random_edge//output.log')
    edge_values = []
    with open(random_edge_dir, 'r', encoding='gbk', errors='ignore') as f:
        lines = f.readlines()  # 读取所有行
        for line in lines:
            value = line.split(':')[-1].strip()  # 获取冒号后面的数值
            edge_values.append(float(value))

    # 根据读取到的随机边数据初始化 DataFrame
    df_all['random_edge'] = edge_values

    # 读取 random_neighbor 的数据
    random_neighbor_dir = os.path.join(folder_path, 'random_neighbor//output.log')
    nei_values = []
    with open(random_neighbor_dir, 'r', encoding='gbk', errors='ignore') as f:
        lines = f.readlines()  # 读取所有行
        for line in lines:
            value = line.split(':')[-1].strip()  # 获取冒号后面的数值
            nei_values.append(float(value))

    # 对齐random_jump的长度与df_all的长度
    if len(nei_values) < len(df_all):
        nei_values.extend([None] * (len(df_all) - len(nei_values)))  # 填充缺失值
    elif len(nei_values) > len(df_all):
        nei_values = nei_values[:len(df_all)]  # 截断多余的值

    # 添加random_neighbor列
    df_all['random_neighbor'] = nei_values

    # 保存到一个 Excel 文件
    output_file = os.path.join(folder_path, f'{folder_name}.xlsx')
    df_all.to_excel(output_file, index=False)
    print(f"数据已成功保存到 {output_file}")


# 处理 BA_1 到 BA_5 文件夹
for i in range(1, 6):
    folder_name = f'BA_{i}'
    process_folder(folder_name)
