"""
数据预处理
"""
import pandas as pd

# 导入数据
data = pd.read_csv('./data/credit_card.csv', encoding='gbk')

# ---------------------数据清洗
# 清理瑕疵户异常数据
#   如果是瑕疵户，那么逾期、呆账、强制停卡记录、退票、拒往记录至少有一个为1
#   如果不是，那么响应的数据都必须为2
data = data[(data['瑕疵户'] == 2) & (data['逾期'] == 2) & (data['呆账'] == 2)
            & (data['强制停卡记录'] == 2) & (data['退票'] == 2) & (data['拒往记录'] == 2)
            |
            ((data['瑕疵户'] == 1) & ((data['逾期'] == 1) | (data['呆账'] == 1) | (data['强制停卡记录'] == 1) |
                                   (data['退票'] == 1) | (data['拒往记录'] == 1)))]

# 针对频率属性存在“不使用”这一取值，对应的刷卡额应该在20000以下
data = data[~((data['频率'] == 5) & (data['月刷卡额'] != 1))]

# 处理未知的家庭月收入
data.loc[(data['个人月收入'] == 7) | (data['个人月收入'] == 8), '家庭月收入'] = 6


def func(li, title):
    for i in range(len(li)):
        data.loc[data[title] == i + 1, title] = li[i]


# 将数据改为以万元为单位显示（取区间最大值）
# 个人月收入
li1 = [0, 1, 2, 3, 4, 5, 6, 8]
func(li1, '个人月收入')
# 个人月开销
li2 = [1, 2, 3, 4, 6]
func(li2, '个人月开销')
# 家庭月收入
li3 = [2, 4, 6, 8, 10, 12]
func(li3, '家庭月收入')
# 月刷卡额
li4 = [2, 4, 6, 8, 10, 15, 20, 30]
func(li4, '月刷卡额')

data.reset_index(inplace=True)

# ---------------------属性构建
# 历史信用风险属性
data['历史信用'] = 0
for i in range(data.shape[0]):
    data.loc[i, '历史信用'] += 1 if data.loc[i, '瑕疵户'] == 1 else 0
    data.loc[i, '历史信用'] += 2 if data.loc[i, '逾期'] == 1 else 0
    data.loc[i, '历史信用'] += 3 if data.loc[i, '呆账'] == 1 else 0
    data.loc[i, '历史信用'] += 3 if data.loc[i, '强制停卡记录'] == 1 else 0
    data.loc[i, '历史信用'] += 3 if data.loc[i, '退票'] == 1 else 0
    data.loc[i, '历史信用'] += 3 if data.loc[i, '拒往记录'] == 1 else 0

# 经济风险
data['经济风险'] = 0
for i in range(data.shape[0]):
    if data.loc[i, '月刷卡额'] <= data.loc[i, '个人月收入']:
        if data.loc[i, '借款余额'] == 1:
            data.loc[i, '经济风险'] += 1
    # elif data.loc[i, '月刷卡额'] > data.loc[i, '个人月收入'] and (data.loc[i, '月刷卡额'] <= data.loc[i, '家庭月收入']):
    elif data.loc[i, '个人月收入'] < data.loc[i, '月刷卡额'] <= data.loc[i, '家庭月收入']:
        if data.loc[i, '借款余额'] == 1:
            data.loc[i, '经济风险'] += 2
        else:
            data.loc[i, '经济风险'] += 1
    elif data.loc[i, '月刷卡额'] > data.loc[i, '家庭月收入']:
        if data.loc[i, '借款余额'] == 1:
            data.loc[i, '经济风险'] += 4
        else:
            data.loc[i, '经济风险'] += 2
    if data.loc[i, '个人月开销'] <= data.loc[i, '月刷卡额']:
        data.loc[i, '经济风险'] += 1

# 收入风险
data['收入风险'] = 0
for i in range(data.shape[0]):
    if data.loc[i, '住家'] in [1, 2, 6]:
        data.loc[i, '收入风险'] += 1
    if data.loc[i, '职业'] <= 7 or data.loc[i, '职业'] in [19, 21]:
        data.loc[i, '收入风险'] += 2
    elif (15 <= data.loc[i, '职业'] <= 17) or data.loc[i, '职业'] in [20, 22]:
        data.loc[i, '收入风险'] += 1
    if data.loc[i, '年龄'] <= 2:
        data.loc[i, '收入风险'] += 1

# 将处理的数据导出去
data.to_csv('./data/process.csv', index=None, encoding='gbk')

# z-score
# arr1 = preprocessing.scale(data['历史信用'].values)
# arr2 = preprocessing.scale(data['经济风险'].values)
# arr3 = preprocessing.scale(data['收入风险'].values)
# # 导出csv
# dataframe = pd.DataFrame({'历史信用风险': arr1, '经济风险': arr2, '收入风险': arr3})
# dataframe.to_csv("./data/process.csv", index=False, sep=',', encoding='gbk')
