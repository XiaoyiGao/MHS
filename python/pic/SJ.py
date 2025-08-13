import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as mticker

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
    'sub_jump_1': [],
    'sub_jump_2': [],
    'sub_jump_3': [],
    'sub_jump_4': []
}

# 遍历所有k值
for k in parameter_values:
    base_path = f'C://Users//Lenovo//Desktop//code//SSA_test//{parameter}//{parameter}_{k}//{model}//'

    # 临时保存当前k值下的所有试验结果
    temp_results = {
        'sub_jump_1': [],
        'sub_jump_2': [],
        'sub_jump_3': [],
        'sub_jump_4': []
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

# 自定义颜色、标签和点样式
colors = ['black', 'black', 'black', 'black']  # All lines black
labels = [r'$\eta$=1', r'$\eta$=2', r'$\eta$=3', r'$\eta$=4']
markers = ['o', 's', '^', 'x']  # 圆形、方块、三角形、十字形
fillstyles = ['none', 'none', 'none', 'none']  # Hollow markers

# 创建图表
plt.figure(figsize=(10, 8))
x = parameter_values # 横轴为k的取值

# 绘制三条策略的折线
for i, key in enumerate(results_by_strategy.keys()):
    plt.plot(
        x,
        results_by_strategy[key],
        marker=markers[i],
        markerfacecolor='none',  # Make markers hollow
        markeredgecolor=colors[i],  # Marker edge color
        markersize=24,  # Slightly smaller markers
        linewidth=2,
        color=colors[i],
        label=labels[i],
        fillstyle=fillstyles[i]  # Ensure markers are hollow
    )

# 设置坐标轴格式
plt.gca().yaxis.set_major_formatter(mticker.FuncFormatter(lambda y, _: f'{y/10000:.2f}'))
plt.gca().yaxis.set_major_locator(mticker.LinearLocator(3))
#plt.ylim(0, 150)
#plt.xlim(left= 0)  # 设置横轴从0开始
#plt.ylim(bottom=0)  # 设置纵轴从0开始

# 设置标签和图例

#plt.xlabel(f'{parameter}', fontsize=25)
plt.xlabel(r'$\mathit{t}$', fontsize=40)  # 使用 \mathit 强制斜体
plt.ylabel(r'$\mathrm{\mathbb{I}}(S)$', fontsize=40, fontweight='bold')
plt.xticks(x, fontsize=40)
plt.yticks(fontsize=40)
#plt.legend(fontsize= 20)
plt.tight_layout()


# 保存图表
#plt.savefig(f"C://Users//Lenovo//Desktop//论文//latex//els-cas-templates//figs//pic//{parameter}_lines_{model}_SJ.pdf", format="pdf")
#plt.show()
plt.savefig(f'C://Users//Lenovo//Desktop//论文//附件//{parameter}_{model}_SJ.pdf', format = 'pdf')
