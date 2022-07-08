"""
数据探索
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

plt.style.use('ggplot')
plt.rcParams['font.sans-serif'] = ['SimHei']

data = pd.read_csv('./data/credit_card.csv', encoding='gbk')
data.info()
des = data.describe()
data.isnull().any(axis=1)
data[data.isnull().values == True]

# ---------------------------客户历史信用记录与瑕疵户的关系
bad_count = data['瑕疵户'].value_counts()
plt.figure()
plt.bar(x=bad_count.index, height=bad_count)
plt.xticks(bad_count.index, labels=['否', '是'])
plt.title('瑕疵户')
plt.ylabel('用户数量')
plt.show()

# 区分瑕疵户与非瑕疵户
xiaci = data[data['瑕疵户'] == 1]
no_xiaci = data[data['瑕疵户'] == 2]


def drow(name):
    labels = ['是', '否']
    width = 0.5
    yes = [len(xiaci[xiaci[name] == 1]) / len(xiaci[name]),
           len(no_xiaci[no_xiaci[name] == 1]) / len(no_xiaci[name])]
    no = [len(xiaci[xiaci[name] == 2]) / len(xiaci[name]),
          len(no_xiaci[no_xiaci[name] == 2]) / len(no_xiaci[name])]
    plt.bar(labels, yes, width, label='是')
    plt.bar(labels, no, width, bottom=yes, label='否')
    plt.ylabel('占比')
    plt.title(name)
    plt.legend()
    plt.show()


# 逾期
drow('逾期')
# 呆账
drow('呆账')
# 强制停卡记录
drow('强制停卡记录')
# 退票
drow('退票')
# 拒往记录
drow('拒往记录')


# -----------------------客户经济情况
def drow2(datas, xlab, lab):
    plt.figure()
    plt.bar(x=datas.index, width=0.2, height=datas)
    plt.xticks(datas.index, labels=lab)
    plt.xlabel(xlab)
    plt.ylabel('数量')
    plt.show()


# 个人月开销
mon = data['个人月开销'].value_counts()
drow2(mon, '个人月开销(万元)', ['1以下', '1-2', '2-3', '3-4', '4以上'])

# 月刷卡额
drow2(data['月刷卡额'].value_counts(), '月刷卡额(万元)',
      ['2以下', '2-4', '4-6', '6-8', '8-10', '10-15', '15-20', '20以上'])

# 个人月收入
drow2(data['个人月收入'].value_counts(), '个人月收入(万元)', ['无收入', '0-1', '1-2', '2-3', '3-4', '4-5', '5-6', '6以上'])

# 家庭月收入
drow2(data['家庭月收入'].value_counts().sort_index(), '家庭月收入(万元)', ['未知', '2以下', '2-4', '4-6', '6-8', '8-10', '10以上'])


# --------------------------------------客户经济风险(个人月收入与家庭月收入的关系)
def func(k):
    li = []
    for i in range(1, 9):
        lab = data[data['个人月收入'] == i]
        li.append(len(lab[lab['家庭月收入'] == k]) / len(lab))
    return li


def drow3():
    """
     未知/无收入， 未知/0-1
     2以下/无收入，2以下/0-1
     2-4/无收入 ， 2-4/0-1
    ....
    """
    labels = ['无收入', '0-1', '1-2', '2-3', '3-4', '4-5', '5-6', '6以上']
    width = 0.4
    weizhi = func(0)
    down2 = func(1)
    to4 = func(2)
    to6 = func(3)
    to8 = func(4)
    to10 = func(5)
    up10 = func(6)
    plt.figure(figsize=(12.8, 5.4))
    plt.bar(labels, weizhi, width, label='未知')
    plt.bar(labels, down2, width, bottom=weizhi, label='2以下')
    plt.bar(labels, to4, width, bottom=np.array(weizhi) + np.array(down2), label='2-4')
    plt.bar(labels, to6, width, bottom=np.array(weizhi) + np.array(down2) + np.array(to4), label='4-6')
    plt.bar(labels, to8, width, bottom=np.array(weizhi) + np.array(down2) + np.array(to4) + np.array(to6), label='6-8')
    plt.bar(labels, to10, width,
            bottom=np.array(weizhi) + np.array(down2) + np.array(to4) + np.array(to6) + np.array(to8),
            label='8-10')
    plt.bar(labels, up10, width,
            bottom=np.array(weizhi) + np.array(down2) + np.array(to4) + np.array(to6) + np.array(to8) + np.array(to10),
            label='10以上')
    plt.title('个人月收入与家庭月收入的关系')
    plt.xlabel('个人月收入(万元)')
    plt.ylabel('占比')
    plt.legend(title='家庭月收入(万元)', bbox_to_anchor=(1, 1))
    plt.show()


drow3()


# ----------------客户经济风险（月刷卡额与个人月收入的关系）
def func1(k):
    li = []
    for i in range(1, 9):
        lab = data[data['月刷卡额'] == i]
        li.append(len(lab[lab['个人月收入'] == k]) / len(lab))
    return li


labels = ['2以下', '2-4', '4-6', '6-8', '8-10', '10-15', '15-20', '20以上']


def drow4():
    no = func1(1)
    down1 = func1(2)
    to2 = func1(3)
    to3 = func1(4)
    to4 = func1(5)
    to5 = func1(6)
    to6 = func1(7)
    up6 = func1(8)
    plt.figure(figsize=(12.8, 5.4))
    plt.bar(labels, no, 0.4, label='无收入')
    plt.bar(labels, down1, 0.4, bottom=no, label='0-1')
    plt.bar(labels, to2, 0.4, bottom=np.array(no) + np.array(down1), label='1-2')
    plt.bar(labels, to3, 0.4, bottom=np.array(no) + np.array(down1) + np.array(to2), label='2-3')
    plt.bar(labels, to4, 0.4, bottom=np.array(no) + np.array(down1) + np.array(to2) + np.array(to3), label='3-4')
    plt.bar(labels, to5, 0.4,
            bottom=np.array(no) + np.array(down1) + np.array(to2) + np.array(to3) + np.array(to4),
            label='4-5')
    plt.bar(labels, to6, 0.4,
            bottom=np.array(no) + np.array(down1) + np.array(to2) + np.array(to3) + np.array(to4) + np.array(to5),
            label='5-6')
    plt.bar(labels, up6, 0.4,
            bottom=np.array(no) + np.array(down1) + np.array(to2) + np.array(to3) +
                   np.array(to4) + np.array(to5) + np.array(to6),
            label='6以上')
    plt.title('月刷卡额与个人月收入的关系')
    plt.xlabel('月刷卡额(万元)')
    plt.ylabel('占比')
    plt.legend(title='个人月收入(万元)', bbox_to_anchor=(1, 1))
    plt.show()


drow4()


# -----------------客户经济风险（月刷卡额与家庭月收入的关系）
def func2(k):
    li = []
    for i in range(1, 9):
        lab = data[data['月刷卡额'] == i]
        li.append(len(lab[lab['家庭月收入'] == k]) / len(lab))
    return li


def drow5():
    weizhi = func2(0)
    down2 = func2(1)
    to4 = func2(2)
    to6 = func2(3)
    to8 = func2(4)
    to10 = func2(5)
    up10 = func2(6)
    plt.figure(figsize=(12.8, 5.4))
    plt.bar(labels, weizhi, 0.4, label='未知')
    plt.bar(labels, down2, 0.4, bottom=weizhi, label='2以下')
    plt.bar(labels, to4, 0.4, bottom=np.array(weizhi) + np.array(down2), label='2-4')
    plt.bar(labels, to6, 0.4, bottom=np.array(weizhi) + np.array(down2) + np.array(to4), label='4-6')
    plt.bar(labels, to8, 0.4, bottom=np.array(weizhi) + np.array(down2) + np.array(to4) + np.array(to6), label='6-8')
    plt.bar(labels, to10, 0.4,
            bottom=np.array(weizhi) + np.array(down2) + np.array(to4) + np.array(to6) + np.array(to8),
            label='8-10')
    plt.bar(labels, up10, 0.4,
            bottom=np.array(weizhi) + np.array(down2) + np.array(to4) + np.array(to6) + np.array(to8) + np.array(to10),
            label='10以上')
    plt.title('月刷卡额与家庭月收入的关系')
    plt.xlabel('月刷卡额(万元)')
    plt.ylabel('占比')
    plt.legend(title='家庭月收入(万元)', bbox_to_anchor=(1, 1))
    plt.show()


drow5()
