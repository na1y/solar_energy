**建立環境**
1. 透過[python -m venv 名稱]，建立虛擬環境
2. 使用CMD，，CD到Scrpits啟動activity，啟動虛擬環境
3. pip install lightgbm optuna pvlib pandas

**資料預處理程式使用步驟**
1. 先使用combine_train_data.py，將舊訓練資料(1~7月)與新的訓練資料結合(9月)。程式內第一個CSV路徑輸入舊的資料集，第二個CSV路徑輸入新的資料集，這樣新資料就會接續在舊資料後面。
2. 新舊資料集都合併後，接著使用combine_train_data.py，輸入L1~L17所在的資料夾位置，此程式會將所有測站的資料，依照測站編號由小到大排序，輸出一個完整的資料集。
3. 
