import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
import pickle  # 用来保存模型和output_uniques变量


# 读取数据集（注意：请确保"penguins-chinese.csv"文件在同一目录下）
penguin_df = pd.read_csv("penguins-chinese.csv", encoding='gbk')

# 删除缺失值所在的行
penguin_df.dropna(inplace=True)

# 将企鹅的种类定义为目标输出变量
output = penguin_df['企鹅的种类']

# 使用企鹅栖息的岛屿、喙的长度、喙的深度、翅膀的长度、身体质量、性别作为特征
features = penguin_df[['企鹅栖息的岛屿', '喙的长度', '喙的深度', '翅膀的长度', '身体质量', '性别']]

# 对特征进行独热编码（One-Hot Encoding）
features = pd.get_dummies(features)

# 将目标输出变量转换为离散数值
output_codes, output_uniques = pd.factorize(output)

# 划分训练集和测试集（训练集80%，测试集20%）
x_train, x_test, y_train, y_test = train_test_split(
    features, output_codes, train_size=0.8, random_state=42  # 加random_state保证结果可复现
)

# 构建并训练随机森林分类器
rfc = RandomForestClassifier()
rfc.fit(x_train, y_train)

# 测试模型准确率
y_pred = rfc.predict(x_test)
score = accuracy_score(y_test, y_pred)
print(f"模型准确率：{score:.2f}")

# 保存模型到rfc_model.pkl
with open('rfc_model1.pkl', 'wb') as f:
    pickle.dump(rfc, f)

# 保存物种映射关系到output_uniques.pkl
with open('output_uniques1.pkl', 'wb') as f:
    pickle.dump(output_uniques, f)

print("保存成功，已生成rfc_model.pkl和output_uniques.pkl文件。")
