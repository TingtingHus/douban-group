# -*- coding: utf-8 -*-
# @Time    : 2020/12/31 下午9:31
# @Author  : Huting
from pyecharts.charts import Geo
from pyecharts.options import ComponentTitleOpts
from pyecharts.components import Table
from pyecharts.faker import Faker
from pyecharts import options as opts
import pandas as pd
import datetime
import numpy as np
import re

pattern = re.compile(r'[\u4e00-\u9fa5]+')


# 表格组件
def Table_bas(header_list,row_list,title):
    table = Table()
    table.add(header_list, row_list)
    table.set_global_opts(
        title_opts=ComponentTitleOpts(title=title)
    )
    return table


# 中国地图数据
def Geo_base(provs_list,values_list,title):
    geo = (
        Geo(is_ignore_nonexistent_coord=True)
            .add_schema(maptype="china")
            .add(None, [list(z) for z in zip(provs_list,values_list)])
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False),)
            .set_global_opts(
            visualmap_opts=opts.VisualMapOpts(range_color=['#CCEBFF', '#22DDDD', '#0099FF', '#003D66'],)
            , title_opts=opts.TitleOpts(title=title)
        )
    )
    return geo


def read_file(f):
    with open(f,'r') as file:
        lines = file.readlines()
        str_lines = str(lines).replace("'", "").replace(r"\n", "")  # 转字符串，便于删除冗余字符
        list_dict = eval(str_lines)
        df = pd.DataFrame(list_dict)
    return df


if __name__ == "__main__":
    name = 'user_info_detail'
    user_info = read_file(name)
    user_info['reg_time'] = pd.to_datetime(user_info['reg_time'],format='%Y/%m/%d')
    user_info[['books','group_num','music','photos','followers','movies','comment']] = user_info[['books','group_num','music','photos','followers','movies','comment']].apply(pd.to_numeric)
    user_info = user_info.fillna(0)

    # # 2.活跃用户画像：平均加入小组数、平均豆瓣年龄、平均粉丝数、平均读书数、平均观影数、平均标记专辑数、平均相册数、平均影评数
    # headers = ["指标","平均数","众数","中位数"]
    # rows = [
    #     ["加入小组数",user_info['group_num'].mean().round(decimals=2),user_info['group_num'].mode().tolist()[0],user_info['group_num'].median()],
    #     ["豆瓣用户年龄",((datetime.datetime.now() - user_info['reg_time'])/365.2425).dt.days.mean().round(decimals=2),((datetime.datetime.now() - user_info['reg_time'])/365.2425).dt.days.mode().tolist()[0],((datetime.datetime.now() - user_info['reg_time'])/365.2425).dt.days.median()],
    #     ["粉丝数",user_info['followers'].mean().round(decimals=2),user_info['followers'].mode().tolist()[0],user_info['followers'].median()],
    #     ["读书数",user_info['books'].mean().round(decimals=2),user_info['books'].mode().tolist()[0],user_info['books'].median()],
    #     ["观影数",user_info['movies'].mean().round(decimals=2),user_info['movies'].mode().tolist()[0],user_info['movies'].median()],
    #     ["专辑数",user_info['music'].mean().round(decimals=2),user_info['music'].mode().tolist()[0],user_info['music'].median()],
    #     ["相册数",user_info['photos'].mean().round(decimals=2),user_info['photos'].mode().tolist()[0],user_info['photos'].median()],
    # ]
    # table = Table_bas(headers,rows,"豆瓣鹅组活跃用户画像")
    # table.render("豆瓣鹅组活跃用户画像.html")

    # 1.活跃用户地理分布
    user_info['location'] = user_info['location'].apply(lambda x: np.nan if x == np.nan else str(x).encode('utf-8').decode('unicode_escape'))
    user_info['des'] = user_info['location'].apply(lambda x: 0 if len(pattern.findall(x)) == 0 else 1)
    provs = []
    for one in user_info[user_info['des'] == 1].sort_values('location',ascending=True).groupby(['location'])['location'].value_counts().index.tolist():
        provs.append(one[0])
    values = user_info[user_info['des'] == 1].sort_values('location').groupby(['location'])['location'].value_counts().values.tolist()
    geo = Geo_base(provs,values,"豆瓣鹅组活跃用户地理分布")
    geo.render("豆瓣鹅组活跃用户地理分布.html")
