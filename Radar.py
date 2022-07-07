# -*- coding: utf-8 -*-
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号


# K 值寻优
def findk(feature):
    # K值寻优
    SSE = []  # 存放每次结果的误差平方和
    for k in range(1, 9):
        estimator = KMeans(n_clusters=k)  # 构造聚类器
        estimator.fit(feature)
        SSE.append(estimator.inertia_)
    X = range(1, 9)
    plt.xlabel('k')
    plt.ylabel('SSE')
    plt.plot(X, SSE, 'o-')
    plt.show()


# 绘制雷达图，传入参数1：model_center(聚类中心)，参数2：label(特征名字)
def radarplot(model_center=None, label=None):
    n = len(label)  # 特征个数
    # 对labels进行封闭，否则会有因为matplotlib版本引起的错误
    label = np.concatenate((label, [label[0]]))
    # 间隔采样，设置雷达图的角度，用于平分切开一个圆面,endpoint设置为False表示随机采样不包括stop的值
    angles = np.linspace(0, 2 * np.pi, n, endpoint=False)
    # 拼接多个数组，使雷达图一圈封闭起来
    angles = np.concatenate((angles, [angles[0]]))
    # 创建一个空白画布
    fig = plt.figure(figsize=(5, 5))
    # 创建子图，设置极坐标格式，绘制圆形
    ax = fig.add_subplot(1, 1, 1, polar=True)
    # 添加每个特征的标签
    ax.set_thetagrids(angles * 180 / np.pi, label)
    # 设置y轴范围
    ax.set_ylim(model_center.min(), model_center.max())
    # 添加网格线
    ax.grid(True)
    # 设置备选的折线颜色和样式,防止线条重复
    sam = ['r', '0', 'g', 'b', 'm', 'y', 'k', 'p', 'c']
    mak = ['4', '8', 'x', '*', 'd', '_', '.', '+', '|']
    labels = []
    # 循环添加每个类别的线圈
    for i in range(len(model_center)):
        values = np.concatenate((model_center[i], [model_center[i][0]]))
        ax.plot(angles, values, c=sam[i], marker=mak[i])
        plt.yticks(fontsize=15)
        plt.xticks(fontsize=15)
        labels.append('客户群' + str(i))
    plt.legend(labels, fontsize=15)
    plt.show()
