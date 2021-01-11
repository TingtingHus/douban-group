# -*- coding: utf-8 -*-
# @Time    : 2020/12/23 下午3:06
# @Author  : Huting
import json
from collections import defaultdict
import pandas as pd
import numpy as np
import re
import jieba
import gensim
from pyecharts.charts import Bar, HeatMap
from pyecharts import options as opts
from pyecharts.globals import ThemeType
import random


COLORS = ["#5793f3", "#d14a61", "#675bba"]
PATTERN_NUM = re.compile(r'[0-9]+')
group_mapping = {
    "豆瓣吃瓜人才组": "634189",
    "青青草原": "babysheep",
    "豆瓣彩虹组": "634210",
    "豆瓣令组": "674006",
    "豆瓣鹅组": "blabla",
    "豆瓣吃瓜组": "658687",
    "花路情报局": "649504",
    "鹅们栖息地": "qiqier",
    "豆瓣拉踩小组": "lacai",
    "豆瓣艾玛花园": "650302",
    "心碎复健基地": "670255",
    "豆瓣九组": "664519",
    "自由小组": "654153",
    "吃瓜科学家": "664622",
    "豆瓣韩娱": "627382",
    "娱乐净土": "673382",
    "豆瓣婧组": "646388",
    "鹅组来了": "ezu",
    "小象八卦": "613560",
    "旧日议事厅": "682809",
    "豆瓣爽组": "697689",
    "生活组": "586674",
    "哈哈哈哈哈哈哈哈哈哈哈": "638298",
    "逼组": "asshole",
    "就等你上车啦": "669481",
    "人生问题研究社": "677543",
    "上班这件事": "myjob",
    "哇靠": "wakao",
    '豆瓣劝分小组': "652046"
}
# 小组人数
group_member = {
    "豆瓣吃瓜人才组": 553565,
    "青青草原": 464154,
    "豆瓣彩虹组": 331574,
    "豆瓣令组": 102734,
    "豆瓣鹅组": 696036,
    "豆瓣吃瓜组": 168458,
    "花路情报局": 58578,
    "鹅们栖息地": 265009,
    "豆瓣拉踩小组": 55922,
    "豆瓣艾玛花园": 67215,
    "心碎复健基地": 11870,
    "豆瓣九组": 150430,
    "自由小组": 68584,
    "吃瓜科学家": 127020,
    "豆瓣韩娱": 74266,
    "娱乐净土": 17013,
    "豆瓣婧组": 231645,
    "鹅组来了": 391773,
    "小象八卦": 310227,
    "旧日议事厅": 101189,
    "豆瓣爽组": 156781,
    "生活组": 630682,
    "哈哈哈哈哈哈哈哈哈哈哈": 497544,
    "逼组": 1319749,
    "就等你上车啦": 179409,
    "人生问题研究社": 163737,
    "上班这件事": 572764,
    "哇靠": 90757,
    '豆瓣劝分小组': 290091
}


# 热力图
def Heatmap_with_label_show(x_value,values,title):

    heatmap = (
        HeatMap(init_opts=opts.InitOpts(width="900px", height="600px", ))
            .add_xaxis(x_value)
            .add_yaxis(
            None,
            x_value,
            values,
            label_opts=opts.LabelOpts(is_show=True, position="inside"),
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(title=title),
            visualmap_opts=opts.VisualMapOpts(
                min_=0,
                max_=1,
                range_color=['#CCEBFF', '#22DDDD', '#0099FF', '#003D66'],  # 设置主题颜色

            ),
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-45), is_inverse=True)
        )
    )
    return heatmap


# 柱状系列图，单Y轴，翻转XY轴
def Bar_reversal_axis(x, y1_name, y1_values, y2_name, y2_values, y3_name, y3_values,title):
    bar = (
        Bar(init_opts=opts.InitOpts(width="900px", height="600px", theme=ThemeType.LIGHT))
            .add_xaxis(x)
            .add_yaxis(y1_name, y1_values)
            .add_yaxis(y2_name, y2_values)
            .add_yaxis(y3_name, y3_values)
            .reversal_axis()
            .set_series_opts(
            label_opts=opts.LabelOpts(position="right",is_show=False),
            markpoint_opts=opts.MarkPointOpts(
            data=[
                opts.MarkPointItem(type_="max", name="最大值"),
                opts.MarkPointItem(type_="min", name="最小值"),
                opts.MarkPointItem(type_="average", name="平均值"),
            ]),
            )
            .set_global_opts(title_opts=opts.TitleOpts(title=title))
    )
    return bar


# 柱状系列图，单Y轴
def Bar_axis(x, y1_name, y1_values, y2_name, y2_values, y3_name, y3_values,title):
    bar = (
        Bar(init_opts=opts.InitOpts(width="900px", height="600px", theme=ThemeType.LIGHT))
            .add_xaxis(x)
            .add_yaxis(y1_name, y1_values)
            .add_yaxis(y2_name, y2_values)
            .add_yaxis(y3_name, y3_values)
            .set_series_opts(
            label_opts=opts.LabelOpts(is_show=False),
            )
            .set_global_opts(
            title_opts=opts.TitleOpts(title=title),
            # xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-45), is_inverse=True)
        ),
    )
    return bar


# 柱状图，双Y轴（没能实现翻转XY）
def bars_with_two_axis(x, y1_name, y1_values, y2_name, y2_values, title):
    bar = (
        Bar(init_opts=opts.InitOpts(width="1200px", height="600px"))
            .add_xaxis(xaxis_data=x)
            .add_yaxis(series_name=y1_name, y_axis=y1_values, yaxis_index=0, color=COLORS[1])
            .add_yaxis(series_name=y2_name, y_axis=y2_values, yaxis_index=1, color=COLORS[0])
            .extend_axis(
            yaxis=opts.AxisOpts(
                name=y2_name,
                type_="value",
                # min_=0,
                # max_=250,
                position="right",
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(color=COLORS[1])
                ),
                axislabel_opts=opts.LabelOpts(formatter="{value}"),
            )
        )
            .set_global_opts(
            yaxis_opts=opts.AxisOpts(
                type_="value",
                name=y1_name,
                # min_=0,
                # max_=250,
                position="left",
                offset=0,
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(color=COLORS[0])
                ),
                axislabel_opts=opts.LabelOpts(formatter="{value}"),
            ),
            tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
            title_opts=opts.TitleOpts(title=title),
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-45), is_inverse=True),
        )
    )
    return bar


def get_related(x,y):
    retA = [i for i in x if i in y]
    x_y_rel = round((len(retA) / len(x)),2)
    return x_y_rel


def group_word_simavg(string_list_y,string_list_x):
    stopkey = [line.strip() for line in open('scu_stopwords.txt').readlines()]  # 读取停止词(可自定义)文件并保存到列表stopkey
    mylist = []
    for title in string_list_y:
        jiebas = jieba.cut_for_search(title)
        fenci_key = list(set(jiebas) - set(stopkey))  # 将目标短语去掉停用词
        mylist.append(fenci_key)
    dictionary = gensim.corpora.Dictionary(mylist)
    corpus = [dictionary.doc2bow(doc) for doc in mylist]
    tfidf = gensim.models.TfidfModel(corpus)  # 使用TF-IDF模型对语料库建模
    # 分析测试文档与已存在的每个训练文本的相似度
    index = gensim.similarities.SparseMatrixSimilarity(tfidf[corpus], num_features=len(dictionary.keys()))

    result = []
    for word in string_list_x:
        test_doc_list = [word for word in jieba.cut_for_search(word)]
        test_doc_vec = dictionary.doc2bow(test_doc_list)
        sim = index[tfidf[test_doc_vec]]
        result.append(sim)

    string_avg = pd.DataFrame(result).values.mean()
    return round(string_avg,2)


if __name__ == "__main__":

    # 数据准确，获取数据并清洗格式
    topic = pd.read_pickle("topic_df").drop_duplicates(subset=['topic_id'])
    # 错误数据订正
    topic.loc[topic.topic_id == '202721237', 'topic_pub_time'] = '2020-11-28 11:01:14'
    topic.loc[topic.topic_id == '202744351', 'topic_pub_time'] = '2020-11-28 14:39:09'
    topic.loc[topic.topic_id == '202781984', 'topic_pub_time'] = '2020-11-28 20:15:32'
    topic.loc[topic.topic_id == '202811460', 'topic_pub_time'] = '2020-11-29 00:09:32'
    topic.loc[topic.topic_id == '202817918', 'topic_pub_time'] = '2020-11-29 01:39:40'
    topic.loc[topic.topic_id == '202820996', 'topic_pub_time'] = '2020-11-29 03:40:45'
    topic.loc[topic.topic_id == '202853741', 'topic_pub_time'] = '2020-11-29 13:18:22'
    topic.loc[topic.topic_id == '202901882', 'topic_pub_time'] = '2020-11-29 21:04:12'

    topic['topic_pub_time'] = pd.to_datetime(topic['topic_pub_time'], format='%Y/%m/%d %H')
    topic[['topic_id', 'zan', 'collect']] = topic[['topic_id', 'zan', 'collect']].apply(pd.to_numeric)
    topic['transmit'] = topic['transmit'].str.strip('[').str.strip(']').str.strip("'").apply(pd.to_numeric)
    topic['topic_day'] = topic['topic_pub_time'].dt.day
    # 读取reply
    reply = pd.read_pickle("reply_df").drop_duplicates(subset=['topic_id', 'reply_id', 'reply_pub_time'])
    reply['reply_pub_time'] = pd.to_datetime(reply['reply_pub_time'], format='%Y/%m/%d %H')
    reply['reply_zan'] = reply['reply_zan'].str.strip('[').str.strip(']').str.strip("'").apply(pd.to_numeric)
    reply['reply_day'] = reply['reply_pub_time'].dt.day
    # 将两个表连接
    reply_topic = reply.merge(topic, left_on=['group', 'topic_id'],
                              right_on=['group', 'topic_id'])  # 默认inner取交集，结果为reply的行
    # 由于wakao、670255、674006 664622采样周期中帖子数较少，平均回复数干扰较大，故剔除，研究总样本小组共26个
    reply_topic_new = reply_topic.drop(
        reply_topic[(reply_topic['group'] == 'wakao') | (reply_topic['group'] == '670255') | (
                reply_topic['group'] == '674006')| (reply_topic['group'] == '664622')].index)

    # 数据可视化
    # 将小组id映射成小组名
    new_group_map = {v: k for k, v in group_mapping.items()}

    # # 5.各小组平均日发帖数、话题平均回复数
    # # 平均日发帖数
    # reply_topic_count = reply_topic_new[['group', 'topic_id']].drop_duplicates().groupby('group')['topic_id'].count()
    # group_topic_avg = reply_topic_count / 2  # 两天的发帖数，求日均所以要除以2
    # group_topic_avg_x = group_topic_avg.sort_values().index.to_series().tolist()
    # group_topic_avg_y = group_topic_avg.sort_values().tolist()
    # group_topic_avg_x_name = [new_group_map[x] if x in new_group_map else x for x in group_topic_avg_x]
    #
    # pic5_1 = Bar_reversal_axis(group_topic_avg_x_name,'日发帖数',group_topic_avg_y,None,None,None,None,'各小组日均发帖数')
    # pic5_1.render('各小组日均发帖数.html')
    #
    # # 话题平均回复数
    # reply_sum = reply_topic_new.groupby('group')['topic_id'].count()
    # topic_reply_avg = (reply_sum / reply_topic_count).round(decimals=2)
    # topic_reply_avg_x = topic_reply_avg.sort_values().index.to_series().tolist()
    # topic_reply_avg_y = topic_reply_avg.sort_values().tolist()
    # topic_reply_avg_x_name = [new_group_map[x] if x in new_group_map else x for x in topic_reply_avg_x]
    #
    # pic5_2 = Bar_reversal_axis(topic_reply_avg_x_name,'话题平均回复数',topic_reply_avg_y,None,None,None,None,'各小组话题平均回复数')
    # pic5_2.render('各小组话题平均回复数.html')
    #
    # # 为将两个指标画到同一坐标系，需要按日均发帖小组顺序输出
    # topic_reply_avg_df = pd.DataFrame(topic_reply_avg)
    # topic_reply_avg_df = topic_reply_avg_df.reset_index()
    # topic_reply_avg_df['group'] = topic_reply_avg_df['group'].astype('category')
    # topic_reply_avg_df['group'].cat.set_categories(group_topic_avg_x, inplace=True)
    # topic_reply_avg_df.sort_values('group', ascending=True,inplace=True)
    # topic_reply_avg_df.set_index(['group'])
    # topic_reply_avg_index_new = pd.Series(topic_reply_avg_df['topic_id'].values, index=topic_reply_avg_df['group'])
    #
    # topic_reply_avg_index_new_x = topic_reply_avg_index_new.index.to_series().tolist()
    # topic_reply_avg_index_new_y = topic_reply_avg_index_new.tolist()
    # topic_reply_avg_index_new_x_name = [new_group_map[x] if x in new_group_map else x for x in topic_reply_avg_index_new_x]
    #
    # pic5 = bars_with_two_axis(group_topic_avg_x_name,'日发帖数',group_topic_avg_y,'话题平均回复数',topic_reply_avg_index_new_y,title='各小组平均日发帖数及话题平均回复数')
    # pic5.render('各小组平均日发帖数及话题平均回复数.html')

    # # 1.各小组日均活跃人数、成员日均活跃度
    # reply_topic_pep1 = reply_topic_new[['group','topic_owner']].rename(columns={'topic_owner': 'reply_id_2'})
    # reply_topic_pep2 = reply_topic_new[['group','reply_id_2']]
    # row_concat = pd.concat([reply_topic_pep1, reply_topic_pep2]).drop_duplicates()
    # # 日均活跃人数
    # reply_pep_avg = (row_concat.groupby('group')['reply_id_2'].count() / 2).round(decimals=2)
    # reply_pep_avg_x = reply_pep_avg.sort_values().index.to_series().tolist()
    # reply_pep_avg_y = reply_pep_avg.sort_values().tolist()
    # reply_pep_avg_x_name = [new_group_map[x] if x in new_group_map else x for x in reply_pep_avg_x]
    # pic1_1 = Bar_reversal_axis(x=reply_pep_avg_x_name,y1_name='日均活跃人数',y1_values=reply_pep_avg_y,y2_name=None,y2_values=None,title='各小组日均活跃人数')
    # pic1_1.render('各小组日均活跃人数.html')
    #
    # # 导出鹅组活跃客户id
    # # bazu_id_list = row_concat.loc[row_concat.group == 'blabla',['reply_id_2']]['reply_id_2'].drop_duplicates().values.tolist()
    # # with open('user_bazu', 'a+') as f:
    # #     f.write(json.dumps(bazu_id_list).encode("utf-8").decode("utf-8") + "\n")
    #
    # # 成员回复活跃度
    # reply_sum = reply_topic_new.groupby(['group'])['reply_id_2'].count()
    # reply_pep = reply_topic_pep2.drop_duplicates().groupby(['group'])['reply_id_2'].count()
    # member_reply_avg = (reply_sum / reply_pep).round(decimals=2)
    # member_reply_avg_x = member_reply_avg.sort_values().index.to_series().tolist()
    # member_reply_avg_y = member_reply_avg.sort_values().tolist()
    # member_reply_avg_x_name = [new_group_map[x] if x in new_group_map else x for x in member_reply_avg_x]
    # pic1_2 = Bar_reversal_axis(x=member_reply_avg_x_name,y1_name='成员回复活跃度',y1_values=member_reply_avg_y,y2_name=None,y2_values=None,title='各小组成员回复活跃度')
    # pic1_2.render('各小组成员回复活跃度.html')

    # # 2.各小组29号均留存率(28号29号发布的帖子对应的用户留存率）
    # user_day1 = reply_topic_new[['group', 'topic_owner', 'topic_day']].rename(columns={'topic_owner': 'reply_id_2', 'topic_day': 'reply_day'})
    # user_day2 = reply_topic_new[['group', 'reply_id_2', 'reply_day']]
    # user_days_act = pd.concat([user_day1, user_day2]).drop_duplicates()
    # user_days_act_groupby = user_days_act.groupby(['group', 'reply_id_2'])
    # # 29号留存率
    # # user_days_restore = pd.DataFrame(columns=['group', 'reply_id_2', '29号留存']) # 匹配下面的Dataframe.append
    # user_days_dict = defaultdict(list)
    # for name, group in user_days_act_groupby:
    #     restore = 1 if set(group['reply_day'].values.tolist()) >= set([28, 29]) else 0
    #     user_days_dict['group'].append(name[0])
    #     user_days_dict['reply_id_2'].append(name[1])
    #     user_days_dict['29号留存'].append(restore)
    #     # 用Dataframe.append是可以的，但是速度非常慢，故不用下面这条语句，改用user_days_dict
    #     # user_days_restore = user_days_restore.append({'group': name[0], 'reply_id_2': name[1], '29号留存': restore}, ignore_index=True)
    # user_days_restore = pd.DataFrame(user_days_dict)
    # user_group_29_28 = user_days_restore.groupby(['group'])['29号留存'].sum()
    # user_group_28 = user_days_act[user_days_act['reply_day'] == 28].groupby(['group'])['reply_id_2'].count()
    # user_group_29 = (user_group_29_28 / user_group_28).round(decimals=2)
    # user_group_29_x = user_group_29.sort_values().index.to_series().tolist()
    # user_group_29_y = user_group_29.sort_values().tolist()
    # user_group_29_x_name = [new_group_map[x] if x in new_group_map else x for x in user_group_29_x]
    # pic2 = Bar_reversal_axis(x=user_group_29_x_name,y1_name='29号留存率',y1_values=user_group_29_y,y2_name=None,y2_values=None,title='各小组29号均留存率')
    # pic2.render('各小组29号均留存率.html')

    # # 8.各小组话题热度延续度
    # # 非当日回复数占所有回复数比
    # reply_days = reply_topic_new[['group', 'reply_id_2','topic_pub_time','topic_day','reply_pub_time','reply_day']]
    # reply_days_hot = reply_days.loc[reply_days['reply_day'] != reply_days['topic_day'],]
    # reply_hot_count = reply_days_hot.groupby(['group'])['reply_id_2'].count()
    # # reply_sum 来自5.话题平均回复数-总回复数
    # reply_hot_ratio = (reply_hot_count / reply_sum).round(decimals=2)
    # reply_hot_ratio_x = reply_hot_ratio.sort_values().index.to_series().tolist()
    # reply_hot_ratio_y = reply_hot_ratio.sort_values().tolist()
    # reply_hot_ratio_x_name = [new_group_map[x] if x in new_group_map else x for x in reply_hot_ratio_x]
    # pic8 = Bar_reversal_axis(x=reply_hot_ratio_x_name,y1_name='非当日回复数占所有回复数的比',y1_values=reply_hot_ratio_y,y2_name=None,y2_values=None,title='各小组非当日回复数占所有回复数的比')
    # pic8.render('各小组非当日回复数占所有回复数的比.html')

    # # 3.各小组间成员重合度（热力图）
    # # 小组回复id数，row_concat来自1
    # user_related = row_concat.groupby(['group'])['reply_id_2'].count()
    # user_related_x = user_related.sort_values().index.to_series().tolist()
    # user_related_x_name = [new_group_map[x] if x in new_group_map else x for x in user_related_x]
    # user_relationship = []
    # for group_x,group_x_name in zip(user_related_x,user_related_x_name):
    #     group_x_value = row_concat.loc[row_concat['group'] == group_x, 'reply_id_2'].tolist()
    #     for group_y,group_y_name in zip(user_related_x,user_related_x_name):
    #         if group_y == group_x:
    #             all_users = row_concat.loc[row_concat['group'] != group_x, 'reply_id_2'].drop_duplicates().tolist()
    #             x_y_relative = round(1 - get_related(group_x_value, all_users),2)
    #             user_relationship.append([group_x_name, group_y_name, x_y_relative])
    #         else:
    #             group_y_value = row_concat.loc[row_concat['group'] == group_y, 'reply_id_2'].tolist()
    #             x_y_relative = get_related(group_x_value, group_y_value)
    #             user_relationship.append([group_x_name,group_y_name,x_y_relative])
    # pic3 = Heatmap_with_label_show(user_related_x_name,user_relationship,'各小组间活跃成员重合度')
    # pic3.render("各小组间活跃成员重合度.html")

    # # 4.用户活跃时间段分布
    # user_active_time1 = reply_topic_new[['group','topic_id','topic_owner','topic_pub_time']].rename(columns={'topic_owner':'reply_id_2','topic_pub_time':'reply_pub_time'}).drop_duplicates()
    # user_active_time2 = reply_topic_new[['group','topic_id','reply_id_2','reply_pub_time']]
    # user_active_time = pd.concat([user_active_time1,user_active_time2]).drop_duplicates()
    # user_active_hour = user_active_time['reply_pub_time'].dt.hour.value_counts(sort=False)
    # user_active_hour_x = user_active_hour.index.to_series().tolist()
    # user_active_hour_y = user_active_hour.tolist()
    # user_active_hour_x_name = [new_group_map[x] if x in new_group_map else x for x in user_active_hour_x]
    # pic4 = Bar_axis(user_active_hour_x_name,'时间',user_active_hour_y,None,None,None,None,"用户活跃时间段分布")
    # pic4.render("用户活跃时间段分布.html")

    # # 6.各小组话题质量：帖子平均点赞数、平均收藏数、平均转发数
    # group_topic_qua = reply_topic_new[['group','topic_id','topic_pub_time', 'topic_title','zan', 'collect', 'transmit']].drop_duplicates()
    # topic_zan = group_topic_qua.fillna(0).sort_values('group', ascending=False).groupby(['group'])['zan'].mean().round(decimals=2)
    # topic_collect = group_topic_qua.fillna(0).sort_values('group', ascending=False).groupby(['group'])['collect'].mean().round(decimals=2)
    # topic_transmit = group_topic_qua.fillna(0).sort_values('group', ascending=False).groupby(['group'])['transmit'].mean().round(decimals=2)
    #
    # # 为将3个指标画到同一坐标系，需要按平均收藏数的小组顺序输出
    # topic_collect_x = topic_collect.sort_values().index.to_series().tolist()
    # topic_collect_y = topic_collect.sort_values().tolist()
    # topic_collect_x_name = [new_group_map[x] if x in new_group_map else x for x in topic_collect_x]
    # # 平均点赞数
    # topic_zan_df = pd.DataFrame(topic_zan)
    # topic_zan_df = topic_zan_df.reset_index()
    # topic_zan_df['group'] = topic_zan_df['group'].astype('category')
    # topic_zan_df['group'].cat.set_categories(topic_collect_x,inplace=True)
    # topic_zan_df.sort_values('group',ascending=True,inplace=True)
    # topic_zan_df.set_index(['group'])
    # topic_zan_index_new = pd.Series(topic_zan_df['zan'].values,index=topic_zan_df['group'])
    # topic_zan_index_new_y = topic_zan_index_new.tolist()
    #
    # # 平均转发数
    # topic_transmit_df = pd.DataFrame(topic_transmit)
    # topic_transmit_df = topic_transmit_df.reset_index()
    # topic_transmit_df['group'] = topic_transmit_df['group'].astype('category')
    # topic_transmit_df['group'].cat.set_categories(topic_collect_x,inplace=True)
    # topic_transmit_df.sort_values('group',ascending=True,inplace=True)
    # topic_transmit_df.set_index(['group'])
    # topic_transmit_index_new = pd.Series(topic_transmit_df['transmit'].values,index=topic_transmit_df['group'])
    # topic_transmit_index_new_y = topic_transmit_index_new.tolist()
    #
    # pic6 = Bar_reversal_axis(topic_collect_x_name,'平均收藏数',topic_collect_y,'平均点赞数',topic_zan_index_new_y,'平均转发数',topic_transmit_index_new_y,"各小组话题质量")
    # pic6.render("各小组话题质量.html")

    # # 7.各小组回复质量：最赞top5平均点赞数、全部回复平均点赞数
    # group_reply_qua = reply_topic_new[['group','topic_id','reply_pub_time', 'reply_zan', 'reply_id_2']].drop_duplicates()
    # reply_zan_all_avg = group_reply_qua.fillna(0).sort_values(['group'], ascending=False).groupby(['group'])['reply_zan'].mean().round(decimals=2)
    # reply_zan_top = group_reply_qua.fillna(0).sort_values(['group','reply_zan'], ascending=[0,0]).groupby(['group','topic_id']).head(5)
    # reply_zan_top_avg = reply_zan_top.sort_values(['group'], ascending=False).groupby(['group'])['reply_zan'].mean().round(decimals=2)
    # reply_zan_top_avg_x = reply_zan_top_avg.sort_values().index.to_series().tolist()
    # reply_zan_top_avg_y = reply_zan_top_avg.sort_values().tolist()
    # reply_pep_avg_x_name = [new_group_map[x] if x in new_group_map else x for x in reply_zan_top_avg_x]
    #
    # # 为将两个指标画到同一坐标系，需要按最赞top5平均点赞数的小组顺序输出
    # reply_zan_all_avg_df = pd.DataFrame(reply_zan_all_avg)
    # reply_zan_all_avg_df = reply_zan_all_avg_df.reset_index()
    # reply_zan_all_avg_df['group'] = reply_zan_all_avg_df['group'].astype('category')
    # reply_zan_all_avg_df['group'].cat.set_categories(reply_zan_top_avg_x, inplace=True)
    # reply_zan_all_avg_df.sort_values('group', ascending=True,inplace=True)
    # reply_zan_all_avg_df.set_index(['group'])
    # reply_zan_all_avg_index_new = pd.Series(reply_zan_all_avg_df['reply_zan'].values, index=reply_zan_all_avg_df['group'])
    # reply_zan_all_avg_index_new_y = reply_zan_all_avg_index_new.tolist()
    # pic7 = Bar_reversal_axis(reply_pep_avg_x_name,'最赞top5平均点赞数',reply_zan_top_avg_y,'全部回复平均点赞数',reply_zan_all_avg_index_new_y,None,None,"各小组回复质量")
    # pic7.render("各小组回复质量.html")

    # # 9.各小组28号29号帖子标题分词近似度（数据效果不是很好）
    # group_topic_title = reply_topic_new[['group','topic_id','topic_title']].drop_duplicates()
    # group_title = group_topic_title.sort_values(['group'], ascending=False).groupby(['group'])['topic_id'].count()
    # group_title_x = group_title.sort_values().index.to_series().tolist()
    # group_title_x_name = [new_group_map[x] if x in new_group_map else x for x in group_title_x]
    # titles_relationship = []
    # for group_x,group_x_name in zip(group_title_x,group_title_x_name):
    #     group_x_value = group_topic_title.loc[group_topic_title['group'] == group_x, 'topic_title'].drop_duplicates().tolist()
    #     for group_y,group_y_name in zip(group_title_x,group_title_x_name):
    #         if group_y == group_x:
    #             all_titles = group_topic_title.loc[group_topic_title['group'] != group_x, 'topic_title'].drop_duplicates().tolist()
    #             x_y_relative = round(1 - group_word_simavg(all_titles, group_x_value),2)
    #             titles_relationship.append([group_x_name, group_y_name, x_y_relative])
    #         else:
    #             group_y_value = group_topic_title.loc[group_topic_title['group'] == group_y, 'topic_title'].drop_duplicates().tolist()
    #             x_y_relative = group_word_simavg(group_y_value, group_x_value)
    #             titles_relationship.append([group_x_name,group_y_name,x_y_relative])
    # pic9 = Heatmap_with_label_show(group_title_x_name,titles_relationship,'各小组28号29号话题分词近似度')
    # pic9.render("各小组28号29号话题分词近似度.html")