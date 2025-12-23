import pandas as pd
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

def train_optimized_model(data_path, save_path):
    # 1. 加载数据（严格检查列名）
    print(f"加载数据：{data_path}")
    try:
        df = pd.read_csv(data_path)
        df.columns = df.columns.str.strip()
        # 必需列定义
        required_cols = [
            '专业', '性别', '每周学习时长（小时）', '上课出勤率', 
            '期中考试分数', '作业完成率', '期末考试分数'
        ]
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            print(f"错误：CSV缺少必需列：{missing_cols}")
            return False
        df = df[required_cols].copy()
        df = df.dropna(how='all')
        print(f"数据加载完成，共{len(df)}行有效数据")
    except FileNotFoundError:
        print(f"错误：未找到CSV文件{data_path}")
        return False

    # 2. 数据预处理
    numeric_cols = [
        '每周学习时长（小时）', '上课出勤率', '期中考试分数', 
        '作业完成率', '期末考试分数'
    ]
    # 强制数值类型+按专业填充缺失值
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
        df[col] = df.groupby('专业')[col].transform(lambda x: x.fillna(x.mean()))

    # 3. 特征编码
    df['性别_编码'] = df['性别'].map({'男': 1, '女': 0})
    df['专业_编码'] = pd.factorize(df['专业'])[0]

    # 4. 特征筛选（强制保留出勤率）
    numeric_features = numeric_cols + ['性别_编码', '专业_编码']
    numeric_df = df[numeric_features].copy()
    corr_with_target = numeric_df.corr()['期末考试分数'].abs().sort_values(ascending=False)
    selected_features = corr_with_target[corr_with_target > 0.2].index.tolist()
    selected_features = [col for col in selected_features if col != '期末考试分数']
    
    # 强制保留必要特征
    must_have = ['上课出勤率', '每周学习时长（小时）', '期中考试分数', '作业完成率']
    for col in must_have:
        if col not in selected_features:
            selected_features.append(col)
    print(f"最终筛选特征：{selected_features}")

    # 5. 模型训练
    X = numeric_df[selected_features]
    y = df['期末考试分数']
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    X_train, X_val, y_train, y_val = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

    model = RandomForestRegressor(n_estimators=150, max_depth=6, min_samples_split=8, random_state=42)
    model.fit(X_train, y_train)

    # 6. 模型评估
    y_pred = model.predict(X_val)
    mae = mean_absolute_error(y_val, y_pred)
    r2 = r2_score(y_val, y_pred)
    print(f"模型评估 - 平均绝对误差：{mae:.2f} | 决定系数R²：{r2:.2f}")

    # 7. 保存模型+预处理数据
    try:
        joblib.dump({
            'model': model,
            'scaler': scaler,
            'selected_features': selected_features,
            'gender_map': {'男': 1, '女': 0},
            'major_encoder': dict(zip(df['专业'], df['专业_编码'])),
            'attendance_col': '上课出勤率'
        }, save_path)
        # 保存预处理后的数据
        df.to_csv(r"D:\streamlit_env\processed_data.csv", index=False, encoding='utf-8')
        print(f"模型保存至：{save_path}")
        print(f"预处理数据保存至：D:\\streamlit_env\\processed_data.csv")
        return True
    except Exception as e:
        print(f"保存失败：{str(e)}")
        return False

if __name__ == "__main__":
    # 请确保CSV文件路径正确
    DATA_PATH = r"D:\streamlit_env\student_data_adjusted_rounded.csv"
    MODEL_PATH = r"D:\streamlit_env\optimized_score_model.pkl"
    success = train_optimized_model(DATA_PATH, MODEL_PATH)
    if not success:
        print("\n❌ 模型训练失败，请检查CSV文件路径和列名")
    else:
        print("\n✅ 模型训练完成！")