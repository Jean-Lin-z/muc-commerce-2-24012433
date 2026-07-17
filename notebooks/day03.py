from pathlib import Path
import pandas as pd


DATA_DIR = Path('data')
CSV_PATH = DATA_DIR / '淘宝全品类全国数据.csv'


print('当前工作目录：', Path.cwd())
print('数据文件存在：', CSV_PATH.exists())


df = pd.read_csv(CSV_PATH)
print("="*60)
print("【任务1：读取并初步观察数据】")
print('数据规模(行数,列数)：', df.shape)
print('全部字段名：', df.columns.tolist())
print("前5行数据：")
print(df.head(5))
print("数据整体信息：")
print(df.info())



print("\n" + "="*60)
print("【任务2：字段类型与缺失值】")
print("各字段数据类型：")
print(df.dtypes)

# 缺失值数量 降序排序
missing_count = df.isna().sum().sort_values(ascending=False)
print("\n各字段缺失值数量：")
print(missing_count)

# 缺失百分比
missing_rate = (df.isna().mean() * 100).round(1).sort_values(ascending=False)
print("\n各字段缺失占比(%)：")
print(missing_rate)
"""
字段分析说明：
1. 可直接数值统计：商品价格，dtype为float浮点型，纯数字无文本，支持均值、中位数等计算
2. 暂不宜数值统计：商品销量，字段为object字符串，包含"100+、1万+"等文字分段，无法直接加减求平均
"""


print("\n" + "="*60)
print("【任务3：数据选取】")
# 单列 Series
price_series = df['商品价格']
print("单列类型df['商品价格']：", type(price_series))

# 多列 DataFrame
product_view = df[['商品id', '一级品类', '商品价格', '省份', '商品销量']]
print("\n多列视图product_view类型：", type(product_view))
print("商品基础视图前5行：")
print(product_view.head())

# loc 按标签选取前5行、指定列
print("\nloc选取前5行，一级品类/商品价格/省份：")
print(df.loc[0:4, ['一级品类', '商品价格', '省份']])

# iloc 按位置选取前5行，前4列
print("\niloc选取前5行、前4列：")
print(df.iloc[0:5, 0:4])
"""
df["商品价格"] 与 df[["商品价格"]] 区别：
1. df["商品价格"]：单中括号，返回Series一维序列，只有一列无表头
2. df[["商品价格"]]：双中括号，返回DataFrame二维表格，保留表格结构与列名
"""


print("\n" + "="*60)
print("【任务4：条件筛选与排序】")
# 1. 单条件：广东省全部商品
guangdong = df[df['省份'] == '广东']
# 2. 多条件：广东 且 价格≥1000
condition = (df['省份'] == '广东') & (df['商品价格'] >= 1000)
# 指定字段 + 价格降序
selected_cols = ['商品id', '一级品类', '二级品类', '商品价格', '省份', '商品销量']
gd_high = df.loc[condition, selected_cols].sort_values(by='商品价格', ascending=False)
print("广东价格≥1000商品，价格从高到低前10条：")
print(gd_high.head(10))

# 或条件：浙江/江苏商品，统计数量
zj_js = df[(df['省份'] == '浙江') | (df['省份'] == '江苏')]
print(f"\n浙江或江苏商品总条数：{zj_js.shape[0]}")


print("\n" + "="*60)
print("【任务5：统计与品类分组】")
# 商品价格描述统计
price_desc = df['商品价格'].describe().round(2)
print("商品价格描述统计：")
print(price_desc)

# 一级品类商品数量
cat_count = df['一级品类'].value_counts()
print("\n各一级品类商品数量：")
print(cat_count)

# 分组统计：商品数、均价、中位价，均价降序
category_summary = df.groupby('一级品类').agg(
    商品数=('商品id', 'size'),
    平均价格=('商品价格', 'mean'),
    中位价格=('商品价格', 'median')
).round(2).sort_values('平均价格', ascending=False)
print("\n一级品类价格汇总表：")
print(category_summary)


print("\n" + "="*60)
print("【挑战任务：省份对比 广东VS江苏】")
# 筛选两省数据
target_provinces = ['广东', '江苏']
prov_data = df[df['省份'].isin(target_provinces)]

# 按省份分组统计
prov_summary = prov_data.groupby('省份').agg(
    商品数=('商品id', 'size'),
    平均价格=('商品价格', 'mean'),
    中位价格=('商品价格', 'median')
).round(2)
print("两省商品汇总：")
print(prov_summary)

# 分别输出两省销量最高一级品类
for p in target_provinces:
    top_cat = prov_data[prov_data['省份'] == p]['一级品类'].value_counts().head(1)
    print(f"\n{p} 商品数量最多一级品类：")
    print(top_cat)