# -*- coding: utf-8 -*-
# @Time    : 2020/12/23 下午3:07
# @Author  : Huting
import pandas as pd
import numpy as np


# topic
# my_df = pd.DataFrame(
#     columns=['group', 'topic_id', 'topic_pub_time', 'topic_title', 'topic_owner', 'zan', 'collect', 'transmit'])
# text = 'topic'

# reply
# my_df = pd.DataFrame(
#     columns=['group', 'topic_id', 'reply_id', 'reply_pub_time', 'reply_zan', 'reply_id_2'])
text = 'reply'


# 按行读取，动态分配内存，速度慢
# def read_df(df,file):
#     my_dict = {}
#     with open(file, 'r') as f:
#         lines = f.readlines()
#         for line in lines:
#             print(line)
#             my_dict = eval(line)
#             df = df.append(my_dict, ignore_index=True)
#     return df


# 整体读数据，再生成dataframe，速度快
def read_df(file):
    with open(file, 'r') as f:
        lines = f.readlines()
        str_lines = str(lines).replace("'", "").replace(r"\n", "")  # 转字符串，便于删除冗余字符
        list_dict = eval(str_lines)   # 从字符串转回包含字典的列表
        df = pd.DataFrame(list_dict)
    return df


if __name__ == "__main__":
    my_dataframe = read_df(text)
    print(my_dataframe)
    # 解决汉字编码的问题
    for col in my_dataframe.columns:
        if my_dataframe[col].dtype == object:
            my_dataframe[col] = my_dataframe[col].apply(
                lambda x: np.nan if x == np.nan else str(x).encode('utf-8', 'replace').decode('utf-8'))

    my_dataframe.to_pickle("reply_df")