import pandas as pd
import numpy as np

np.random.seed(24)
df = pd.DataFrame({'A': np.linspace(1, 10, 10)})
df = pd.concat([df, pd.DataFrame(np.random.randn(10, 4), columns=list('BCDE'))],
               axis=1)
df.iloc[0, 2] = np.nan


#设置一般的颜色,设置所有的值小于0的时候，设置颜色为红色
def color_negative_red(val):
    """

    :param val:dataFrame所有满足条件的值
    :return: 带有颜色的值
    """
    color = 'red' if val < 0 else 'black'
    return 'color: %s' % color
#使用方法
s = df.style.applymap(color_negative_red)

#设置某一列的最大值颜色为黄色背景
def highlight_max(s):
    """

    :param s:dataFrame里面的所有值
    :return:
    """
    is_max = s == s.max()
    return ['background-color: yellow' if v else '' for v in is_max]
#使用方法
df.style.apply(highlight_max)
#applymap是按照元素设置，apply是按照列设置

def highlight_max(data, color='yellow'):
    """

    :param data: dataFrame 列/行 取决于axis参数 None 0 1
    :param color:
    :return:
    """
    attr = 'background-color: {}'.format(color)
    if data.ndim == 1:  # Series from .apply(axis=0) or axis=1
        is_max = data == data.max()
        return [attr if v else '' for v in is_max]
    else:  # from .apply(axis=None)
        is_max = data == data.max().max()
        return pd.DataFrame(np.where(is_max, attr, ''),
                            index=data.index, columns=data.columns)

#c = '1'
#a,b = '1','2'
#  d = a == c  ----> d =True

#用法
df.style.apply(highlight_max, color='darkorange', axis=None) #1 每一列的最大值 0 每一行的最大值

#切分指定列样式用法
df.style.apply(highlight_max, subset=['B', 'C', 'D']) #指定列逻辑

#指定范围内标记
df.style.applymap(color_negative_red,subset=pd.IndexSlice[2:5, ['B', 'D']]) #指定范围内标记

#整个DataFrame转化为百分比显示

df.style.format("{:.2%}")

#使用字典指定列格式化
df.style.format({'B': "{:0<4.0f}", 'D': '{:+.2f}'})
#指定B列保留两位小数，格式化B列值显示
df.style.format({"B": lambda x: "±{:.2f}".format(abs(x))})

#内置颜色函数，Nan以红色显示
df.style.highlight_null(null_color='red')

#热力图表显示excel，可以导出为excel
import seaborn as sns

cm = sns.light_palette("green", as_cmap=True)

s = df.style.background_gradient(cmap=cm)

#指定区间热力图表
df.loc[:4].style.background_gradient(cmap='viridis')
#指定区间热力图表 Nan值以指定颜色填充
(df.loc[:4].style.background_gradient(cmap='viridis', low=.2, high=0).highlight_null('red'))

#整张表背景颜色指定，文字颜色指定，以及边框 (不可导出为excel）
df.style.set_properties(**{'background-color': 'black',
                           'color': 'lawngreen',
                           'border-color': 'red',
                           })
#数字单元格bar图，导出excel 不显示
s = df.style.bar(subset=['A', 'B'], color='#d65f5f')
#多列指定不同颜色，待研究
df.style.bar(subset=['A', 'B'], align='mid', color=['#d65f5f', '#5fba7d'])

