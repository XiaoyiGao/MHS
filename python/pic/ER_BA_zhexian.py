import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as mticker

model = "BA"    # ER, BA
n = 1
b = 0.8
t = 0.01
p = 0
parameter = 'k'
parameter_values = [1, 5, 10, 20]  # 横轴上的k取值

# 六个策略的结果，按k的顺序保存
results_by_strategy = {
    'sub_jump_1': [],
    'sub_jump_2': [],
    'sub_jump_3': [],
    'sub_jump_4': [],
    'random_choice': [],
    'random_jump': []
}

# 遍历所有k值
for k in parameter_values:
    base_path = f'C://Users//Lenovo//Desktop//code//SSA_test//{parameter}//{parameter}_{k}//{model}//'

    # 临时保存当前k值下的所有试验结果
    temp_results = {
        'sub_jump_1': [],
        'sub_jump_2': [],
        'sub_jump_3': [],
        'sub_jump_4': [],
        'random_choice': [],
        'random_jump': []
    }

    # 遍历 BA_1 到 BA_3 文件夹
    for i in range(1, 4):
        folder_name = f'{model}_{i}'
        file_path = os.path.join(base_path, folder_name, f'{folder_name}.xlsx')

        if not os.path.exists(file_path):
            continue

        df = pd.read_excel(file_path)

        # 提取每种策略的最后一行值
        for key in temp_results:
            temp_results[key].append(df[key].iloc[-1])

    # 计算每个策略在当前k下的平均值
    for key in results_by_strategy:
        avg = sum(temp_results[key]) / len(temp_results[key]) if temp_results[key] else 0
        results_by_strategy[key].append(avg)

# 自定义颜色与标签
colors = ['tab:red', 'tab:orange', 'tab:blue', 'tab:green', 'tab:purple', 'tab:brown']
labels = ['SJ(1)', 'SJ(2)', 'SJ(3)', 'SJ(4)', 'RC', 'RJ']

# 创建图表
plt.figure(figsize=(10, 6))
x = parameter_values  # 横轴为k的取值

# 绘制六条策略的折线
for i, key in enumerate(results_by_strategy.keys()):
    plt.plot(x, results_by_strategy[key], marker='o', linewidth=2.5, color=colors[i], label=labels[i])

# 设置坐标轴格式
plt.gca().yaxis.set_major_formatter(mticker.FuncFormatter(lambda y, _: f'{y/10000:.2f}'))
plt.gca().yaxis.set_major_locator(mticker.LinearLocator(5))
plt.xlim(left=0)  # 设置横轴从0开始
# 设置标签和图例
plt.xlabel('Parameter k', fontsize=25, fontweight='bold')
plt.ylabel(r'$\mathrm{\mathbb{I}}(S)$', fontsize=26, fontweight='bold')
plt.xticks(x, fontsize=20)
plt.yticks(fontsize=20)
plt.legend(fontsize=18)
plt.tight_layout()

# 保存图表
#plt.savefig(f"C://Users//Lenovo//Desktop//论文//latex//els-cas-templates//figs//pic//k_lines_all.pdf", format="pdf")
plt.show()
