import pandas as pd
import os

def preprocess_and_merge_data(input_folder, output_file):
    all_data = []  # 用於存放所有處理過的資料

    # 獲取資料夾中所有CSV檔案的路徑，並按檔名排序
    file_list = sorted([os.path.join(input_folder, f) for f in os.listdir(input_folder) if f.endswith('.csv')])

    for file in file_list:
        print(f"正在處理檔案: {file}")

        # 載入 CSV 檔案
        data = pd.read_csv(file)

        # 確保 DateTime 欄位轉換為 datetime 格式，然後格式化為 YYYYMMDDHHMM
        if 'DateTime' in data.columns:
            data['DateTime'] = pd.to_datetime(data['DateTime'])
            data['DateTime'] = data['DateTime'].dt.strftime('%Y%m%d%H%M')

        # 將處理後的資料存入列表
        all_data.append(data)

    # 合併所有資料
    merged_data = pd.concat(all_data, ignore_index=True)

    # 將合併後的資料輸出到指定的CSV文件
    merged_data.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"所有資料已成功合併並輸出到檔案: {output_file}")


# 主程式入口
if __name__ == "__main__":
    # 設定資料夾和輸出檔案名稱
    input_folder = "36_TrainingData"  # 替換為存放17個CSV檔案的資料夾路徑
    output_file = "combine_train_data.csv"  # 輸出檔案名稱

    # 呼叫處理函數
    preprocess_and_merge_data(input_folder, output_file)
