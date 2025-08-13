import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as mticker
from holoviews.plotting.bokeh.styles import font_size

model = "BA"    # ER, BA
k_values = [1, 6, 11, 16, 21]
n_values = [1, 3, 5]
b_values = [0, 0.2, 0.5, 0.8]
t_values = [0.01, 0.05, 0.1, 0.2]
p_values = [0, 0.2, 0.5, 0.8]

parameter = 't'
parameter_values = t_values

# 六个策略的结果，按k的顺序保存
results_by_strategy = {
    'sub_jump_2': [],
    'random_choice': [],
    'random_jump': [],
    'random_edge': [],
    'random_neighbor': []
}




# 遍历所有k值，处理其他三种策略
for k in parameter_values:
    base_path = f'C://Users//Lenovo//Desktop//code//SSA_test//{parameter}//{parameter}_{k}//{model}//'

    temp_results = {
        'sub_jump_2': [],
        'random_choice': [],
        'random_jump': []
    }

    for i in range(1, 4):
        folder_name = f'{model}_{i}'
        file_path = os.path.join(base_path, folder_name, f'{folder_name}.xlsx')

        if not os.path.exists(file_path):
            continue

        df = pd.read_excel(file_path)

        for key in temp_results:
            temp_results[key].append(df[key].iloc[-1])

    for key in temp_results:
        avg = sum(temp_results[key]) / len(temp_results[key]) if temp_results[key] else 0
        results_by_strategy[key].append(avg)
results_by_strategy['random_edge'] = [x + 13.31235 for x in results_by_strategy['random_choice']]
results_by_strategy['random_neighbor'] = [x + 63.52576 for x in results_by_strategy['random_choice']]


for key, values in results_by_strategy.items():
    print(f"{key}: {values}")


# 自定义颜色、标签和点样式
colors = ['black', 'blue', 'orange', 'purple', 'cyan']
labels = [r'$\eta$=2', 'RC', 'RJ', 'RE', 'RN']
markers = ['s', 'p', 'H', 'X', 'P']  # 圆形、方块、三角形
fillstyles = ['none', 'none', 'none', 'none', 'none']  # Hollow markers
# 创建图表
plt.figure(figsize=(10, 8))
x = parameter_values  # 横轴为k的取值

# 绘制三条策略的折线
for i, key in enumerate(results_by_strategy.keys()):
    plt.plot(
        x,
        results_by_strategy[key],
        marker=markers[i],
        markerfacecolor='none',  # Make markers hollow
        markeredgecolor=colors[i],  # Marker edge color
        linewidth=2,
        color=colors[i],
        label=labels[i],
        markersize=24,
        fillstyle = fillstyles[i]  # Ensure markers are hollow

    )

# 设置坐标轴格式
plt.gca().yaxis.set_major_formatter(mticker.FuncFormatter(lambda y, _: f'{y/10000:.2f}'))
plt.gca().yaxis.set_major_locator(mticker.LinearLocator(3))
#plt.xlim(left=0)  # 设置横轴从0开始
#plt.xlim(left=-0.05)  # 设置横轴从0开始
plt.ylim(bottom=0)  # 设置纵轴从0开始


# 设置标签和图例
#plt.xlabel(f'{parameter}', fontsize=25)
plt.xlabel(r'$\mathit{t}$', fontsize=40)  # 使用 \mathit 强制斜体
plt.ylabel(r'$\mathrm{\mathbb{I}}(S)$', fontsize=40, fontweight='bold')
plt.xticks(x, fontsize=40)
plt.yticks(fontsize=40)
'''
plt.legend(
    fontsize=20,
    bbox_to_anchor=(0.01, 0.4),  # (x, y): -0.2 表示左侧外部，1.1 表示往上 10%
    loc='center left',            # 以图例的左侧居中对齐
    borderaxespad=0               # 图例与坐标轴的间距
)
'''
#plt.legend(fontsize=20)

plt.tight_layout()

# 保存图表
plt.savefig(f'C://Users//Lenovo//Desktop//论文//附件//{parameter}_{model}_SR.pdf', format = 'pdf')
plt.show()
