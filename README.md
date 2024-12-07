**建立環境**
1. 透過[python -m venv 名稱]，建立虛擬環境
2. 使用CMD，CD到Scrpits啟動activity，啟動虛擬環境
3. pip install lightgbm optuna pvlib pandas

**資料預處理程式使用步驟**
1. 先使用combine_train_data.py，將舊訓練資料(1~7月)與新的訓練資料結合(9月)。程式內第一個CSV路徑輸入舊的資料集，第二個CSV路徑輸入新的資料集，這樣新資料就會接續在舊資料後面。
2. 新舊資料集都合併後，接著使用data_preprocessing.py，輸入L1~L17所在的資料夾位置，此程式會將所有測站的資料，依照測站編號由小到大排序，輸出一個完整的訓練資料集。(處理時，會將DateTime調整成%Y%m%d%H%M格式)
3. 統整成一個完整訓練資料集後，使用add_external_data.py增加外部的特徵於訓練資料集與upload.csv中，後續用於訓練與預測。(擴增中央氣象觀測站的資料)
4. 後續再單獨用pvlib對訓練資料集與upload.csv再擴增，apparent_zenith與apparent_elevation，使用sun_position.py。(擴增PVlib模擬資料)
5. 使用split_datetime.py切割訓練時間部分(目前格式由步驟2處理成%Y%m%d%H%M)，將訓練資料集中的時間切個成年、月、日、時、分等欄位。
   
預處理程式使用順序：combine_train_data.py => data_preprocessing.py => add_external_data.py => sun_position.py => split_datetime.py
上述步驟完成後，即完成預處理

**模型訓練**
1. 使用tune.py指定好訓練資料集後，study.optimize(objective, n_trials=n)調整n決定要訓找幾輪參數，全部完成後於console輸出最佳的參數。
2. 使用model_training_lightGBM.py指定好訓練資料集後，根據tune.py所找出的最佳參依序填入。
3. 使用predict_lightgbm.py指定好訓練好的模型路徑與upload.csv的路徑，將輸出output_with_predictions_lightgbm.csv為結果
