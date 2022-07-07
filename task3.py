"""
构建信用卡高风险客户识别模型
"""
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from Radar import findk, radarplot


data = pd.read_csv('./data/process.csv', encoding='gbk')

# 标准化
sc = StandardScaler()
# 需要标准化的列
data_feature = data[['历史信用', '经济风险', '收入风险']]
feature = sc.fit_transform(data_feature)

# 寻找最优k值，k=3
findk(feature)

# 聚类
model = KMeans(n_clusters=3, random_state=0)
model.fit(feature)  # 训练
center = model.cluster_centers_  # 聚类中心
lab = model.labels_  # 聚类类别

# 雷达图
radarplot(center, data_feature.columns)
