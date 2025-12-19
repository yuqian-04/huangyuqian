# save_model.py (添加调试信息)
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
import pickle

# 设置输出右对齐，防止中文不对齐
pd.set_option('display.unicode.east_asian_width', True)
# 读取数据集，并将字符编码指定为 gbk，防止中文报错
insurance_df = pd.read_csv('insurance-chinese.csv', encoding='gbk')

# 将医疗费用定义为目标输出变量
output = insurance_df['医疗费用']

# 使用年龄、性别、BMI、子女数量、是否吸烟、区域作为特征列
features = insurance_df[['年龄','性别','BMI','子女数量','是否吸烟','区域']]
# 对特征列进行独热编码
features = pd.get_dummies(features)

# 打印特征列名称，用于调试
print("特征列名称（训练时）：")
print(features.columns.tolist())
print(f"\n特征数量：{len(features.columns)}")

# 划分训练集和测试集
x_train, x_test, y_train, y_test = train_test_split(features, output, train_size=0.8, random_state=42)

# 构建随机森林回归模型并训练
rfr = RandomForestRegressor(random_state=42)
rfr.fit(x_train, y_train)

# 用训练好的模型对测试集数据进行预测
y_pred = rfr.predict(x_test)

# 计算模型的可决系数（R-squared）
r2 = r2_score(y_test, y_pred)
print(f"\n模型R²分数: {r2:.4f}")

# 使用Pickle保存训练好的模型到文件
with open('rfr_model.pkl', 'wb') as f:
    pickle.dump(rfr, f)

# 同时保存特征列信息，便于Web应用使用
with open('model_features.pkl', 'wb') as f:
    pickle.dump({
        'feature_names': features.columns.tolist(),
        'feature_order': features.columns.tolist()
    }, f)

print('保存成功，已生成相关文件。')
