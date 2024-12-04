import os
import pandas as pd
import numpy as np
import lightgbm as lgb
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from datetime import datetime
import joblib  # 用於保存縮放器

# 設定隨機種子
def set_seed(seed=42):
    np.random.seed(seed)

set_seed(42)

# 1. 讀取資料
data = pd.read_csv("total_data_temp_windspeed_Precp_SunShine.csv")

# 確保目標變數為數值型
data['Power(mW)'] = pd.to_numeric(data['Power(mW)'], errors='coerce')

# 增加週期性特徵
data['Hour_sin'] = np.sin(2 * np.pi * data['Hours'] / 24)
data['Hour_cos'] = np.cos(2 * np.pi * data['Hours'] / 24)
data['Month_sin'] = np.sin(2 * np.pi * data['Month'] / 12)
data['Month_cos'] = np.cos(2 * np.pi * data['Month'] / 12)

# 選擇特徵與目標變數
X = data[['LocationCode', 'Month', 'Day', 'Hours', 'Minute', 
          'Temperature', 'WindSpeed', 'Precp', 'apparent_zenith', 'apparent_elevation', 'GlobalRad']]
y = data['Power(mW)']

# 特徵縮放 (MinMaxScaler)
scaler_X = MinMaxScaler()
scaler_y = MinMaxScaler()

X_scaled = scaler_X.fit_transform(X)
y_scaled = scaler_y.fit_transform(y.values.reshape(-1, 1)).flatten()

# 保存縮放器
scaler_dir = "./models_lightgbm/scalers_lightgbm/"
os.makedirs(scaler_dir, exist_ok=True)
scaler_X_path = os.path.join(scaler_dir, "scaler_X.pkl")
scaler_y_path = os.path.join(scaler_dir, "scaler_y.pkl")

joblib.dump(scaler_X, scaler_X_path)
joblib.dump(scaler_y, scaler_y_path)
print(f"特徵縮放器已保存至: {scaler_X_path} 和 {scaler_y_path}")

# 2. 切分資料集
X_train, X_val, y_train, y_val = train_test_split(X_scaled, y_scaled, test_size=0.2, random_state=42)

train_data = lgb.Dataset(X_train, label=y_train)
val_data = lgb.Dataset(X_val, label=y_val)

# 3. 定義 LightGBM 參數
params = {
    'objective': 'tweedie',
    'metric': 'rmse',
    'boosting_type': 'gbdt',
    'learning_rate': 0.07321224742265185,
    'num_leaves': 200,
    'max_depth': 13,
    'feature_fraction': 0.937105883643767,
    'bagging_fraction': 0.6997629720282448,
    'bagging_freq': 5,
    'lambda_l1': 1.21702199884783,
    'lambda_l2': 1.1581951656373426,
    'verbose': -1,
    'random_state': 42
}


# 4. 訓練 LightGBM 模型
print("開始訓練 LightGBM 模型...")
num_boost_round = 2279
model = lgb.train(
    params,
    train_data,
    num_boost_round=num_boost_round,
    valid_sets=[train_data, val_data],  # 添加驗證集
    valid_names=["train", "valid"],  # 顯示訓練和驗證的 loss
    callbacks=[
        lgb.log_evaluation(period=100),  # 每 100 次迭代輸出 RMSE
        lgb.early_stopping(stopping_rounds=50)  # 提早停止，避免過擬合
    ]
)
print("LightGBM 模型訓練完成！")

# 5. 保存模型
model_dir = "./models_lightgbm/"
os.makedirs(model_dir, exist_ok=True)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
model_path = os.path.join(model_dir, f"lightgbm_model_{timestamp}.txt")

model.save_model(model_path)
print(f"模型已保存至: {model_path}")
