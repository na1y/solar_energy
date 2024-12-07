import pandas as pd

# 讀取 CSV 檔案
file_path = 'total_data_nosplittime_temp_windspeed_Precp_SunShine_sunposition.csv'  # 替換為你的檔案路徑
data = pd.read_csv(file_path)

# 確保 DateTime 欄位為字串格式
data['DateTime'] = data['DateTime'].astype(str)

# 拆分 DateTime 欄位
data['Year'] = data['DateTime'].str[:4].astype(int)
data['Month'] = data['DateTime'].str[4:6].astype(int)
data['Day'] = data['DateTime'].str[6:8].astype(int)
data['Hours'] = data['DateTime'].str[8:10].astype(int)
data['Minute'] = data['DateTime'].str[10:12].astype(int)

# 插入新欄位到指定位置
data.insert(1, 'Year', data.pop('Year'))
data.insert(2, 'Month', data.pop('Month'))
data.insert(3, 'Day', data.pop('Day'))
data.insert(4, 'Hours', data.pop('Hours'))
data.insert(5, 'Minute', data.pop('Minute'))

# 刪除原始 DateTime 欄位
data = data.drop(columns=['DateTime'])

# 儲存結果到新的 CSV 檔案
output_file = 'total_data_temp_windspeed_Precp_SunShine.csv'  # 替換為輸出的檔案名稱
data.to_csv(output_file, index=False, encoding='utf-8-sig')

print("處理完成，檔案已儲存為:", output_file)
