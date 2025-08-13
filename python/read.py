import os
import pandas as pd

# 基础路径
base_code_path = r"C:\Users\lenovo\Desktop\code\SSA_test\add\real_data\21k"

# 输出文件路径
output_excel = r"C:\Users\lenovo\Desktop\code\SSA_test\add\real_data\21k\21k_LT.xlsx"

# 子文件夹与列名映射
folder_col_map = [
    ("s1", "sub_jump_1"),
    ("s2", "sub_jump_2"),
    ("s3", "sub_jump_3"),
    ("s4", "sub_jump_4"),
    ("rc", "random_choice"),
    ("rj", "random_jump"),
    ("re", "random_edge"),
    ("rn", "random_neighbor")
]

def extract_numbers_from_log(filepath):
    """提取 output.log 每行冒号后的浮点数"""
    numbers = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            if ":" in line:
                num_str = line.strip().split(":")[-1]
                try:
                    num = float(num_str)
                except ValueError:
                    num = None
                numbers.append(num)
    return numbers

def pad_list(lst, length):
    """将列表补齐到指定长度"""
    return lst + [None] * (length - len(lst))

# 存储所有列数据
data_dict = {}

for folder, col_name in folder_col_map:
    log_path = os.path.join(base_code_path, folder, "output.log")
    if not os.path.exists(log_path):
        print(f"警告：{log_path} 不存在，列 {col_name} 将为空")
        numbers = []
    else:
        numbers = extract_numbers_from_log(log_path)
    data_dict[col_name] = numbers

# 对齐所有列长度
max_len = max(len(lst) for lst in data_dict.values())
for col in data_dict:
    data_dict[col] = pad_list(data_dict[col], max_len)

# 按要求顺序生成 DataFrame
col_order = [
    "sub_jump_1", "sub_jump_2", "sub_jump_3", "sub_jump_4",
    "random_choice", "random_jump", "random_edge", "random_neighbor"
]
df = pd.DataFrame({col: data_dict[col] for col in col_order})

# 保存 Excel
df.to_excel(output_excel, index=False)
print(f"处理完成，结果已保存到：{output_excel}")
