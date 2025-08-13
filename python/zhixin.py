import os
import pandas as pd
from scipy import stats
import numpy as np

folder_path = r"C:\Users\lenovo\Desktop\论文\picture\real_data"
output_file = r"C:\Users\lenovo\Desktop\论文\picture\real_data\summary_confidence_intervals.xlsx"

col_to_strategy = {
    'sub_jump_3': 'MHS',
    'random_choice': 'RC',
    'random_jump': 'RJ',
    're_numbers': 'RE',
    'rn_numbers': 'RN'
}

def compute_confidence_interval(data, confidence=0.95):
    n = len(data)
    mean = np.mean(data)
    sem = stats.sem(data)
    if n > 1:
        h = sem * stats.t.ppf((1 + confidence) / 2., n-1)
    else:
        h = 0
    lower = mean - h
    upper = mean + h
    return mean, lower, upper

# 存放所有结果的列表
results = []

for filename in os.listdir(folder_path):
    if filename.endswith('.xlsx'):
        file_path = os.path.join(folder_path, filename)
        print(f"Processing file: {filename}")

        df = pd.read_excel(file_path)
        if not all(col in df.columns for col in col_to_strategy.keys()):
            print(f"Warning: Not all required columns found in {filename}, skipping.")
            continue

        for col, strategy in col_to_strategy.items():
            data = df[col].dropna()
            if len(data) == 0:
                print(f"  {strategy}: no valid data")
                continue
            mean, lower, upper = compute_confidence_interval(data)
            diff = upper - mean
            results.append({
                "文件名": filename,
                "策略": strategy,
                "均值": round(mean, 2),
                "上界差值": round(diff, 2)
            })

# 转成DataFrame并保存Excel
results_df = pd.DataFrame(results)
results_df.to_excel(output_file, index=False)
print(f"Summary saved to {output_file}")
