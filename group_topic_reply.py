# -*- coding: utf-8 -*-
# @Time    : 2020/11/19 上午11:16
# @Author  : Huting
import logging
import random
import re
import sys
import traceback
from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
import json

GROUP_NAME_ID_DIC = {
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
    "哇靠": "wakao",
    '豆瓣劝分小组': "652046"
}
PATTERN_NUM = re.compile(r'[0-9]+')

topic = 202810446

# 以下是测试topic用例
# topic = 201252421
# topic = 201933338    # 完整测试数据，单页
# topic = 196026783      # 完整测试数据，多页
# topic = 201019135    # 非目标组
# topic = 101278157   # 没有访问权限
# topic = 101227637   # 页面不存在

chrome_options = Options()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(options=chrome_options)
cookie = {
    "name": "dbcl2",
    "value": "71452972:v8MNa4YXmDs"
}


def get_topic_info(group_id, topic_id):
    topic_info = dict.fromkeys(
        {'group', 'topic_id', 'topic_pub_time', 'topic_title', 'topic_owner', 'zan', 'collect', 'transmit'})  # topic_owner为用户自定义id
    topic_info['group'] = group_id
    topic_info['topic_id'] = topic_id
    topic_info['topic_pub_time'] = driver.find_element_by_xpath(r'//*[@id="topic-content"]/div[2]/h3/span[2]').text
    topic_info['topic_title'] = driver.find_element_by_xpath(r'//*[@id="content"]/div/div[1]/h1').text
    topic_info['topic_owner'] = \
        driver.find_element_by_xpath(r'//*[@id="topic-content"]/div[2]/h3/span[1]/a').get_attribute('href').split(
            'people/')[
            1].split('/')[0]
    topic_info['zan'] = driver.find_element_by_xpath(r'//*[@id="sep"]/div[1]/a/span[2]').text
    topic_info['collect'] = driver.find_element_by_xpath(r'//*[@id="sep"]/div[2]/a/span[2]').text
    transmit = driver.find_element_by_id('sep').find_element_by_class_name('rec').text
    topic_info['transmit'] = PATTERN_NUM.findall(transmit)
    # print(topic_info)
    with open('topic', 'a+') as f:
        f.write(json.dumps(topic_info).encode("utf-8").decode("utf-8") + "\n")
        f.flush()
    logging.info("{topic_id}: success to get topic info".format(topic_id=topic_id))
    print("{topic_id}: success to get topic info".format(topic_id=topic_id))
    return


def open_new_driver(url):
    time.sleep(random.randint(1, 3))
    driver.get(url)
    return


def get_eacn_reply(group_id, topic_id):
    try:
        reply_detail = dict.fromkeys({'group', 'topic_id', 'reply_id', 'reply_pub_time', 'reply_zan', 'reply_id_2'})  # reply_id 是纯数字原始id
        reply_detail['group'] = group_id
        reply_detail['topic_id'] = topic_id
        replys = driver.find_element_by_xpath(r'//*[@id="comments"]').find_elements_by_tag_name('li')
        for reply in replys:
            reply_detail['reply_id'] = reply.get_attribute('data-author-id')
            reply_detail['reply_pub_time'] = reply.find_elements_by_class_name('pubtime')[0].text
            zan = reply.find_element_by_class_name('comment-vote').text
            reply_detail['reply_zan'] = PATTERN_NUM.findall(zan)
            id_2 = reply.find_elements_by_class_name(r'user-face')[0].find_elements_by_css_selector("a")[
                0].get_attribute('href')
            reply_detail['reply_id_2'] = id_2.split('people/')[1].split('/')[0]
            # print(reply_detail)
            with open('reply', 'a+') as f:
                f.write(json.dumps(reply_detail).encode("utf-8").decode("utf-8") + "\n")
                f.flush()
        logging.info("{topic_id}: success to get this page's data".format(topic_id=topic_id))
        print("{topic_id}: success to get this page's data".format(topic_id=topic_id))

    except:
        exceptionInfo()
        logging.info("{topic_id}: --------------------- meet error when getting each reply".format(topic_id=topic_id))
        print("{topic_id}: --------------------- meet error when getting each reply".format(topic_id=topic_id))
        return


def get_pages(group_id, topic_id):
    logging.info("{topic_id}: topic first page's reply begin".format(topic_id=topic_id))
    print("{topic_id}: topic first page's reply begin".format(topic_id=topic_id))
    get_eacn_reply(group_id, topic_id)
    try:
        flag = driver.find_elements_by_class_name('paginator')
        if len(flag) == 0:
            logging.info("{topic_id}: topic only has one page and next topic".format(topic_id=topic_id))
            print("{topic_id}: topic only has one page and next topic".format(topic_id=topic_id))
            return
        else:
            pages = driver.find_element_by_xpath(r'//*[@id="content"]/div/div[1]/div[5]').text
            max_page = PATTERN_NUM.findall(pages)[-1]
            i = 1
            while i < int(max_page):
                logging.info("{topic_id}: finish current page and begin getting the ({i} + 1)'s page".format(topic_id=topic_id,i=i))
                print("{topic_id}: finish current page and begin getting the ({i} + 1)'s page".format(topic_id=topic_id,i=i))
                page_num = i * 100
                page_home = 'https://www.douban.com/group/topic/' + str(topic_id) + '/?start=' + str(page_num)
                open_new_driver(page_home)
                get_eacn_reply(group_id, topic_id)
                i = i + 1
    except:
        exceptionInfo()
        logging.info("---------------------{topic_id}: fail to get multiple reply page and next topic".format(topic_id=topic_id))
        print("---------------------{topic_id}: fail to get multiple reply page and next topic".format(topic_id=topic_id))
        return


def get_topic(url, num):
    try:
        driver.get(url)
        driver.add_cookie(cookie_dict=cookie)
        driver.get(url)
        if driver.title == '页面不存在':
            logging.info("{num}:  topic not exist now".format(num=num))
            print("{num}:  topic not exist now".format(num=num))
            return
        elif driver.title == '没有访问权限':
            logging.info("{num}: topic no permission to visit".format(num=num))
            print("{num}: topic no permission to visit".format(num=num))
            return
        else:
            href = driver.find_element_by_xpath(r'//*[@id="g-side-info"]/div[1]/div/div[2]/div/a').get_attribute('href')
            group = href.split('group/')[1].split('/')[0]
            if group not in GROUP_NAME_ID_DIC.values():
                logging.info("{num}: topic not belong to group list".format(num=num))
                print("{num}: topic not belong to group list".format(num=num))
                return
            else:
                try:
                    get_topic_info(group, num)
                except:
                    exceptionInfo()
                    logging.info("{num}: ********************** fail to get topic info".format(num=num))
                    print("{num}: ********************** fail to get topic info".format(num=num))

                get_pages(group, num)

    except:
        exceptionInfo()
        logging.info("{num}: ********************** driver can not open topic page".format(num=num))
        print("{num}: ********************** driver can not open topic page".format(num=num))
        return


def exceptionInfo():
    ex_type, ex_val, ex_stack = sys.exc_info()
    logging.info(ex_type)
    logging.info(ex_val)
    print(ex_type)
    print(ex_val)
    for stack in traceback.extract_tb(ex_stack):
        logging.info(stack)
        print(stack)


if __name__ == "__main__":
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    logging.basicConfig(filename='topic.log', level=logging.INFO, format=LOG_FORMAT)
    logging.info("Begin process")

    while topic < 202920716:
        logging.info("{topic}: --->>>topic begining".format(topic=topic))
        print("{topic}: --->>>topic begining".format(topic=topic))
        home = 'https://www.douban.com/group/topic/' + str(topic) + "/"
        get_topic(home, topic)
        logging.info("{topic}: Complete and sleep to next topic".format(topic=topic))
        print("{topic}: Complete and sleep to next topic".format(topic=topic))
        time.sleep(2 + random.randint(0, 3))
        topic = topic + 1

    driver.quit()
    
