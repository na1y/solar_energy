import pandas as pd

# 讀取第一個CSV文件，從第二列開始選取
csv1 = pd.read_csv('36_TrainingData_Additional_V2\L12_Train_2.csv')
csv1_subset = csv1.iloc[:, :]  # iloc[:, 1:] 表示選取所有行和從第二列開始的所有列

# 讀取第二個CSV文件
csv2 = pd.read_csv('data\L12_Train.csv')

result = pd.concat([csv2, csv1_subset], axis=0, ignore_index=True)

# 將結果寫入新的CSV文件
result.to_csv('data\L12_Train.csv', index=False)
