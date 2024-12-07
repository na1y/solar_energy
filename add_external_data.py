import pandas as pd


#------------------------------新增外部特徵於資料集----------------------------------

# 讀取 A.csv 和 B.csv
a_csv_path = 'combine_train_data.csv'  # A.csv 檔案路徑
b_csv_path = 'external_data.csv'  # B.csv 檔案路徑
output_csv_path = 'total_data_nosplittime.csv'  # 輸出的 CSV 檔案路徑

# 讀取 CSV
a_df = pd.read_csv(a_csv_path)
b_df = pd.read_csv(b_csv_path)

# 確保比對欄位為字串格式
a_df['DateTime'] = a_df['DateTime'].astype(str)
b_df['Time'] = b_df['Time'].astype(str)

# 選擇需要加入的欄位，假設 B.CSV 包含 'Temperature', 'Humidity', 'WindSpeed'
columns_to_add = ['Temperature', 'WindSpeed', 'Precp', 'GlobalRad']

# 建立字典加速比對，每個欄位單獨建立字典
column_dicts = {col: dict(zip(b_df['Time'], b_df[col])) for col in columns_to_add}

# 新增欄位到 A.CSV
for col, col_dict in column_dicts.items():
    a_df[col] = a_df['DateTime'].map(col_dict)

# 將結果寫入新的 CSV 檔案
a_df.to_csv(output_csv_path, index=False)

print(f"已完成，結果已儲存至 {output_csv_path}")

#------------------------------新增外部特徵於upload.csv----------------------------------
# import pandas as pd

# # 讀取 A.csv 和 B.csv
# a_csv_path = 'upload.csv'  # A.csv 檔案路徑
# b_csv_path = 'external_data.csv'  # B.csv 檔案路徑
# output_csv_path = 'upload_add_external_data.csv'  # 輸出的 CSV 檔案路徑

# # 讀取 CSV
# a_df = pd.read_csv(a_csv_path)
# b_df = pd.read_csv(b_csv_path)

# # 確保比對欄位為字串格式
# a_df['序號'] = a_df['序號'].astype(str)
# b_df['Time'] = b_df['Time'].astype(str)

# # 去掉 A.csv 的秒數（保留 YYYYMMDDHHMM）
# a_df['DateTime_trimmed'] = a_df['序號'].str[:12]  # 取前 12 位（YYYYMMDDHHMM）

# # 選擇需要加入的欄位，假設 B.CSV 包含 'Temperature', 'Humidity', 'WindSpeed'
# columns_to_add = ['Temperature', 'WindSpeed', 'Precp', 'GlobalRad']

# # 建立字典加速比對，每個欄位單獨建立字典
# column_dicts = {col: dict(zip(b_df['Time'], b_df[col])) for col in columns_to_add}

# # 新增欄位到 A.CSV
# for col, col_dict in column_dicts.items():
#     a_df[col] = a_df['DateTime_trimmed'].map(col_dict)

# # 刪除中間欄位（可選）
# a_df.drop(columns=['DateTime_trimmed'], inplace=True)

# # 將結果寫入新的 CSV 檔案
# a_df.to_csv(output_csv_path, index=False)

# print(f"已完成，結果已儲存至 {output_csv_path}")
