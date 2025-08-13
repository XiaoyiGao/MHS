import pandas as pd
import os

# 基础路径
base_path = 'C://Users//Lenovo//Desktop//SSA_test//k//k_6//BA//'

def process_folder(folder_name):
    """
    处理单个文件夹中的数据
    :param folder_name: 文件夹名称，例如 'BA_1'
    :return: 处理后的 DataFrame
    """
    folder_path = os.path.join(base_path, folder_name)
    df_all = pd.DataFrame()

    # 读取 sub_jump_1 到 sub_jump_6 的数据
    sub_jump_values = []  # 用来存储sub_jump的所有数据
    max_length = 0  # 记录最大长度
    for t in range(1, 5):
        file_path = os.path.join(folder_path, f'sub_jump_{t}//output.log')
        values = []
        with open(file_path, 'r', encoding='gbk', errors='ignore') as f:
            lines = f.readlines()  # 读取所有行
            #lines = lines[:-1]  # 排除最后一行
            for line in lines:
                value = line.split(':')[-1].strip()
                values.append(float(value))
        sub_jump_values.append(values)  # 每次读取的sub_jump数据存储到列表中
        if len(values) > max_length:
            max_length = len(values)  # 更新最大长度

    # 将sub_jump数据按列加入df_all，并填充缺失值
    for t, values in enumerate(sub_jump_values, 1):
        if len(values) < max_length:
            values.extend([None] * (max_length - len(values)))  # 填充缺失值
        df_all[f'sub_jump_{t}'] = values

    # 读取 random_choice 的数据
    random_choice_dir = os.path.join(folder_path, 'random_choice//output.log')
    choice_values = []
    with open(random_choice_dir, 'r', encoding='gbk', errors='ignore') as f:
        lines = f.readlines()  # 读取所有行
        #lines = lines[:-1]  # 排除最后一行
        for line in lines:
            value = line.split(':')[-1].strip()
            choice_values.append(float(value))

    # 对齐random_choice的长度与df_all的长度
    if len(choice_values) < len(df_all):
        choice_values.extend([None] * (len(df_all) - len(choice_values)))  # 填充缺失值
    elif len(choice_values) > len(df_all):
        choice_values = choice_values[:len(df_all)]  # 截断多余的值

    # 添加random_choice列
    df_all['random_choice'] = choice_values

    # 读取 random_jump 的数据（注释掉的部分）
    random_jump_dir = os.path.join(folder_path, 'random_jump//output.log')
    jump_values = []
    with open(random_jump_dir, 'r', encoding='gbk', errors='ignore') as f:
        lines = f.readlines()  # 读取所有行
        #lines = lines[:-1]  # 排除最后一行
        for line in lines:
            value = line.split(':')[-1].strip()
            jump_values.append(float(value))

    # 对齐random_jump的长度与df_all的长度
    if len(jump_values) < len(df_all):
        jump_values.extend([None] * (len(df_all) - len(jump_values)))  # 填充缺失值
    elif len(jump_values) > len(df_all):
        jump_values = jump_values[:len(df_all)]  # 截断多余的值

    # 添加random_jump列
    df_all['random_jump'] = jump_values

    # 保存到一个 Excel 文件
    output_file = os.path.join(folder_path, f'{folder_name}.xlsx')
    df_all.to_excel(output_file, index=False)
    print(f"数据已成功保存到 {output_file}")


# 处理 BA_1 到 BA_10 文件夹
for i in range(1, 5):
    folder_name = f'BA_{i}'
    process_folder(folder_name)