# -*- coding: utf-8 -*-
# @Time    : 2020/11/17 4:15 下午
# @Author  : Huting
import random
import re
import sys
import time
import traceback

import requests
from bs4 import BeautifulSoup
from requests import RequestException


GROUP_YULE_NAME_ID_DIC = {
    "豆瓣吃瓜人才组": "634189",
    "青青草原": "babysheep",
    "豆瓣彩虹组": "634210",
    "豆瓣令组": "674006",
    "豆瓣鹅组": "blabla",
    "豆瓣吃瓜组": "658687",
    "豆瓣火研组": "639264",
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
    '豆瓣劝分小组':"652046"
}


def get_html(url,user_agent):
    response = requests.get(url,headers={
        "User-Agent": user_agent,
        "Referer":"https://www.douban.com/",
        "Origin": "https://www.douban.com",
    })
    try:
        if response.status_code == 200:
            return response.text
        return "response.text != 200"
    except RequestException:
        return None


def get_soup(html):
    soup = BeautifulSoup(html, "html.parser")
    return soup


def get_pages(url,user_agent):
    html = get_html(url,user_agent)
    soup = get_soup(html)
    pages = soup.find("div",attrs={"class":"paginator"}).find('span',attrs={"class":"thispage"}).get('data-total-page')
    # print(pages)
    return pages


def exceptionInfo():
    ex_type, ex_val, ex_stack = sys.exc_info()
    for stack in traceback.extract_tb(ex_stack):
        print(stack)


def group_info(soup,num,user_agent):
    # print(soup)
    group_dict = dict.fromkeys({'name', 'id', 'tags','member','founded','sum'})   # sum 是一共多少帖子，member是成员数
    group_dict["name"] = soup.find("div",attrs={"class":"group-desc"}).find("h1").get_text().strip()
    group_dict["id"] = num
    try:
        tags = soup.find("div",attrs={"class":"group-board"}).find("div",attrs={"class":"group-tags"}).find_all('a')
        tag_list = []
        for tag in tags:
            tag_list.append(tag.get_text())
        group_dict["tags"] = tag_list
    except:
        exceptionInfo()
        print("No tags")
        group_dict["tags"] = ''

    pattern_member = re.compile(r'\([0-9]+\)')
    group_dict["member"] = pattern_member.findall(soup.find("div",attrs={"class":"mod side-nav"}).find("a").get_text())[0].replace("(",'').replace(")",'')

    pattern_founded = re.compile(r'[0-9]+-[0-9]+-[0-9]+')
    group_dict['founded'] = pattern_founded.findall(soup.find("div",attrs={"class":"group-board"}).find('p').get_text().strip())

    sum_link = soup.find("div",attrs={"class":"group-topics-more"}).find('a')['href']
    group_dict['sum'] = get_pages(sum_link,user_agent)
    return group_dict


if __name__ == "__main__":
    user_agents = ['Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
                   'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
                   'Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10',
                   'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2',
                   'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16',
                   'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
                   'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0',
                   'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 UBrowser/4.0.3214.0 Safari/537.36',
                   'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.3.4000 Chrome/30.0.1599.101 Safari/537.36',
                   'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER',
                   'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)']

    group_ids = GROUP_YULE_NAME_ID_DIC.values()
    # # print(group_ids)
    # group_ids = ['682809']

    with open('group_info_revised','a+') as f:
        for group_id in group_ids:
            print("{group} is beigning".format(group=group_id))
            home = "https://www.douban.com/group/"
            group_url = home + str(group_id)
            try:
                group_text = get_html(group_url,user_agents[random.randint(0,10)])
                # print(group_text)
                soups = get_soup(group_text)
                info = group_info(soups,group_id,user_agents[random.randint(0,10)])
                print(info)
                f.write(str(info) + "\n")
                f.flush()
                time.sleep(5 + random.randint(0, 10))
                print("success to get {group} and sleep".format(group=group_id))
            except:
                exceptionInfo()
                print("fail to get {group} and sleep".format(group=group_id))
                time.sleep(120 + random.randint(0, 10))



