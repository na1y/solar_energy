import optuna
import lightgbm as lgb
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import pandas as pd

# 設定隨機種子
def set_seed(seed=42):
    np.random.seed(seed)

set_seed(42)

# 讀取數據
data = pd.read_csv("total_data_temp_windspeed_Precp_SunShine.csv")

# 確保目標變數為數值型
data['Power(mW)'] = pd.to_numeric(data['Power(mW)'], errors='coerce')

# # 增加週期性特徵
# data['Hour_sin'] = np.sin(2 * np.pi * data['Hours'] / 24)
# data['Hour_cos'] = np.cos(2 * np.pi * data['Hours'] / 24)
# data['Month_sin'] = np.sin(2 * np.pi * data['Month'] / 12)
# data['Month_cos'] = np.cos(2 * np.pi * data['Month'] / 12)

# 特徵與目標
X = data[['LocationCode', 'Month', 'Day', 'Hours', 'Minute', 
          'Temperature', 'WindSpeed', 'Precp', 'apparent_zenith', 'apparent_elevation', 'GlobalRad']]
y = data['Power(mW)']

# 特徵縮放
scaler_X = MinMaxScaler()
scaler_y = MinMaxScaler()

X_scaled = scaler_X.fit_transform(X)
y_scaled = scaler_y.fit_transform(y.values.reshape(-1, 1)).flatten()

# 分割訓練集和驗證集
X_train, X_valid, y_train, y_valid = train_test_split(X_scaled, y_scaled, test_size=0.2, random_state=42)

# LightGBM 資料集
train_data = lgb.Dataset(X_train, label=y_train)
valid_data = lgb.Dataset(X_valid, label=y_valid, reference=train_data)

# 定義調參目標函數
def objective(trial):
    # 定義參數空間
    params = {
        'objective': 'tweedie',
        'metric': 'rmse',
        'boosting_type': 'gbdt',
        'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.1),
        'num_leaves': trial.suggest_int('num_leaves', 31, 255),
        'max_depth': trial.suggest_int('max_depth', -1, 15),
        'feature_fraction': trial.suggest_float('feature_fraction', 0.6, 1.0),
        'bagging_fraction': trial.suggest_float('bagging_fraction', 0.6, 1.0),
        'bagging_freq': 5,
        'lambda_l1': trial.suggest_float('lambda_l1', 0, 10.0),
        'lambda_l2': trial.suggest_float('lambda_l2', 0, 10.0),
        'verbose': -1,
        'random_state': 42
    }
    
    # 設置大範圍的 num_boost_round
    num_boost_round = 5000
    early_stopping_rounds = 3  # 早停的迭代次數

    # 訓練模型並進行早停
    model = lgb.train(
        params,
        train_data,
        num_boost_round=num_boost_round,
        valid_sets=[valid_data],
        valid_names=["valid"],
        callbacks=[
            lgb.early_stopping(stopping_rounds=early_stopping_rounds),  # 早停回調
            lgb.log_evaluation(period=100)  # 每 100 次顯示 RMSE
        ]
    )
    
    # 記錄最佳迭代次數
    trial.set_user_attr("best_iteration", model.best_iteration)
    
    # 返回驗證集的最終 RMSE
    return model.best_score["valid"]["rmse"]

# 創建 Optuna 調參實驗
study = optuna.create_study(direction="minimize")
study.optimize(objective, n_trials=30)  # 調參 50 次

# 輸出最佳參數
print("Best trial:")
print(study.best_trial.params)

# 輸出最佳 epoch 數
print(f"最佳迭代次數（epoch）: {study.best_trial.user_attrs['best_iteration']}")
