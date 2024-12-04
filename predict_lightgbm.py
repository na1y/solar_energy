import pandas as pd
import numpy as np
import lightgbm as lgb
from sklearn.preprocessing import MinMaxScaler
import joblib

# 1. 加載 LightGBM 模型與 Scaler
model_path = "./models_lightgbm/lightgbm_model_20241128_233249.txt"  # 替換為您的模型文件名
scaler_X_path = "./models_lightgbm/scalers_lightgbm/scaler_X.pkl"    # 替換為特徵縮放模型文件名
scaler_y_path = "./models_lightgbm/scalers_lightgbm/scaler_y.pkl"    # 替換為目標縮放模型文件名

model = lgb.Booster(model_file=model_path)  # 加載 LightGBM 模型
scaler_X = joblib.load(scaler_X_path)       # 加載特徵縮放器
scaler_y = joblib.load(scaler_y_path)       # 加載目標縮放器

# 2. 數據預處理函數
def preprocess_input(data):
    """
    根據訓練邏輯增加週期性特徵。
    """
    data['Hour_sin'] = np.sin(2 * np.pi * data['Hours'] / 24)
    data['Hour_cos'] = np.cos(2 * np.pi * data['Hours'] / 24)
    data['Month_sin'] = np.sin(2 * np.pi * data['Month'] / 12)
    data['Month_cos'] = np.cos(2 * np.pi * data['Month'] / 12)
    return data

# 3. 多筆數據預測函數
def predict_multiple(model, scaler_X, scaler_y, input_data):
    """
    預測多筆數據。
    """
    # 特徵預處理
    # input_data = preprocess_input(input_data)

    # 特徵縮放
    input_scaled = scaler_X.transform(input_data)

    # 模型預測
    predictions_scaled = model.predict(input_scaled)
    predictions = scaler_y.inverse_transform(predictions_scaled.reshape(-1, 1))
    return predictions.flatten()  # 返回 1D 數組

# 4. 載入 CSV 文件
csv_path = "upload_features_temp_windspeed_precp_sunshine.csv"  # 替換為實際的文件路徑
data = pd.read_csv(csv_path)

# 確保 "序號" 是字符串格式
data['序號'] = data['序號'].astype(str)

# 拆解 "序號" 成模型輸入欄位
data['Year'] = data['序號'].str[:4].astype(int)
data['Month'] = data['序號'].str[4:6].astype(int)
data['Day'] = data['序號'].str[6:8].astype(int)
data['Hours'] = data['序號'].str[8:10].astype(int)
data['Minute'] = data['序號'].str[10:12].astype(int)
data['LocationCode'] = data['序號'].str[12:14].astype(int)

# 構建模型輸入數據
test_data = data[['LocationCode', 'Month', 'Day', 'Hours', 'Minute', 'Temperature', 'WindSpeed', 'Precp', 'apparent_zenith', 'apparent_elevation', 'GlobalRad']]

# 5. 進行預測
predicted_powers = predict_multiple(model, scaler_X, scaler_y, test_data)

# 6. 將預測結果填入原始數據
data['答案'] = predicted_powers.round(2)

# 7. 保存結果
output_path = "output_with_predictions_lightgbm.csv"  # 輸出文件路徑
data[['序號', '答案']].to_csv(output_path, index=False)
print(f"預測結果已保存至: {output_path}")
