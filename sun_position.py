import pandas as pd
import pvlib

#------------------------------新增外部特徵於資料集----------------------------------
# 讀取 CSV 文件 - 
file_path = 'total_data_nosplittime.csv'  # 替換為您的檔案路徑
data = pd.read_csv(file_path)

# 確保 DateTime 格式正確（假設原格式為 YYYYMMDDHHMM）
data['DateTime'] = pd.to_datetime(data['DateTime'], format='%Y%m%d%H%M', errors='coerce')

# 檢查是否有 NaT 值
if data['DateTime'].isna().any():
    print("警告：DateTime 欄位包含無效數據，請檢查！")
    data = data.dropna(subset=['DateTime'])

# 定義地理位置
latitude = 23.8953    # 緯度
longitude = 121.5498  # 經度

# 計算太陽位置
solar_position = pvlib.solarposition.get_solarposition(data['DateTime'], latitude, longitude)

# 確保長度一致
if len(data) != len(solar_position):
    raise ValueError("數據長度不一致，請檢查原始數據或計算過程！")

# 新增計算結果到一個新的 DataFrame
solar_data = pd.DataFrame({
    'apparent_zenith': solar_position['apparent_zenith'].values,
    'apparent_elevation': solar_position['apparent_elevation'].values,
})

# 保留原始的 DateTime 格式為字串，並放回原位置
data['DateTime'] = data['DateTime'].dt.strftime('%Y%m%d%H%M')

# 將 solar_data 插入到 DataFrame 倒數第二欄的位置
insert_position = len(data.columns) - 1  # 倒數第二欄的位置
for col in reversed(solar_data.columns):
    data.insert(insert_position, col, solar_data[col])

# 確保 DateTime 欄位保持在原來的第二欄位置
date_col = data.pop('DateTime')  # 移除 DateTime 欄位
data.insert(1, 'DateTime', date_col)  # 將其插回第二欄

# 儲存結果到新的 CSV 文件，使用 float_format 格式化數值
output_path = 'total_data_nosplittime.csv'
data.to_csv(output_path, index=False, float_format='%.1f')  # 保留小數點後 1 位，無科學記號

print(f"結果已儲存到 {output_path}")

# ------------------------------新增外部特徵於upload.csv----------------------------------

# # 讀取 CSV 文件
# file_path = 'upload_add_external_data.csv'  # 替換為您的檔案路徑
# data = pd.read_csv(file_path)

# # 從 "序號" 欄位提取前 12 位作為時間，並轉換為 DateTime 格式
# data['DateTime'] = pd.to_datetime(data['序號'].astype(str).str[:12], format='%Y%m%d%H%M', errors='coerce')

# # 檢查是否有 NaT 值
# if data['DateTime'].isna().any():
#     print("警告：DateTime 欄位包含無效數據，請檢查！")
#     data = data.dropna(subset=['DateTime'])

# # 定義地理位置
# latitude = 23.8953    # 緯度
# longitude = 121.5498  # 經度

# # 計算太陽位置
# solar_position = pvlib.solarposition.get_solarposition(data['DateTime'], latitude, longitude)

# # 確保長度一致
# if len(data) != len(solar_position):
#     raise ValueError("數據長度不一致，請檢查原始數據或計算過程！")

# # 新增計算結果到一個新的 DataFrame
# solar_data = pd.DataFrame({
#     'apparent_zenith': solar_position['apparent_zenith'].values,
#     'apparent_elevation': solar_position['apparent_elevation'].values,
# })

# # 將 solar_data 插入到 DataFrame 倒數第二欄的位置
# insert_position = len(data.columns) - 1  # 倒數第二欄的位置
# for col in reversed(solar_data.columns):
#     data.insert(insert_position, col, solar_data[col])

# # 移除 DateTime 欄位，因為我們只需要 "序號"
# data = data.drop(columns=['DateTime'])

# # 儲存結果到新的 CSV 文件，使用 float_format 格式化數值
# output_path = 'upload_add_external_data.csv'
# data.to_csv(output_path, index=False, float_format='%.1f')  # 保留小數點後 1 位，無科學記號

# print(f"結果已儲存到 {output_path}")

