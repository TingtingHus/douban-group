# -*- coding: utf-8 -*-
# @Time    : 2020/12/22 下午8:17
# @Author  : Huting
import json
import logging
import re
import sys
import time
import traceback
from selenium import webdriver
import random
from selenium.webdriver.chrome.options import Options


chrome_options = Options()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(options=chrome_options)
# driver = webdriver.Chrome()  # 测试的时候用
cookie = {
    "name": "dbcl2",
    "value": "67184301:tnZ/kFENuIc"
}
PATTERN_NUM = re.compile(r'[0-9]+')
PATTERN_GROUP = re.compile(r'\([0-9]+\)')
PATTERN_FOLLOWER = re.compile(r'被[0-9]+人')
PATTERN_BOOKS = re.compile(r'[0-9]+本读过')
PATTERN_MOVIES = re.compile(r'[0-9]+部看过')
PATTERN_MUSIC = re.compile(r'[0-9]+张听过')
# user_id = 'hutingting33'
# user_id = '85205161'  # 已注销测试
# user_id = '137624545'  # 城市地址为空测试
# user_id = '228979888'  # 全部数据为空测试

# users = ['hutingting33','78602999','85205161','137624545','228979888','228979878']


def exceptionInfo():
    ex_type, ex_val, ex_stack = sys.exc_info()
    logging.info(ex_type)
    logging.info(ex_val)
    print(ex_type)
    print(ex_val)
    for stack in traceback.extract_tb(ex_stack):
        logging.info(stack)
        print(stack)


def get_user_info(user):
    user_info = dict.fromkeys(
        {'user_id', 'reg_time', 'location', 'group_num', 'followers', 'books', 'movies', 'music','comment','photos'})
    user_info['user_id'] = user
    user_info['reg_time'] = driver.find_element_by_class_name('user-info').text.split()[-1].replace('加入','')
    loc = len(driver.find_element_by_xpath(r'//*[@id="profile"]/div/div[2]/div[1]/div').text.split())
    user_info['location'] = driver.find_element_by_xpath(r'//*[@id="profile"]/div/div[2]/div[1]/div/a').text if loc == 4 else ''
    groupnum = driver.find_element_by_xpath('//*[@id="group"]/h2').text if len(driver.find_element_by_id('group').text) != 0 else '(0)'
    user_info['group_num'] = PATTERN_GROUP.findall(groupnum)[0].replace('(','').replace(')','')
    followers = driver.find_element_by_xpath(r'//*[@id="content"]/div/div[2]/p[1]/a').text
    user_info['followers'] = PATTERN_FOLLOWER.findall(followers)[0].replace('被','').replace('人','')
    books = driver.find_element_by_xpath(r'//*[@id="book"]/h2').text if len(driver.find_element_by_id('book').text) != 0 else '0'
    user_info['books'] = PATTERN_BOOKS.findall(books)[0].replace('本读过','') if len(PATTERN_BOOKS.findall(books)) != 0 else '0'
    movies = driver.find_element_by_xpath(r'//*[@id="movie"]/h2').text if len(driver.find_element_by_id('movie').text) != 0 else '0'
    user_info['movies'] = PATTERN_MOVIES.findall(movies)[0].replace('部看过','') if len(PATTERN_MOVIES.findall(movies)) != 0 else '0'
    music = driver.find_element_by_xpath(r'//*[@id="music"]/h2').text if len(driver.find_element_by_id('music').text) != 0 else '0'
    user_info['music'] = PATTERN_MUSIC.findall(music)[0].replace('张听过','') if len(PATTERN_MUSIC.findall(music)) != 0 else '0'
    user_info['comment'] = driver.find_element_by_xpath(r'//*[@id="review"]/h2/span/a').text.replace('评论','') if len(driver.find_element_by_id('review').text) != 0 else 0
    user_info['photos'] = driver.find_element_by_xpath(r'//*[@id="photo"]/h2/span/a[1]').text.replace('创建','') if len(driver.find_element_by_id('photo').text) != 0 else 0

    # print(user_info)
    with open('user_info_detail', 'a+') as f:
        f.write(json.dumps(user_info).encode("utf-8").decode("utf-8") + "\n")
        f.flush()
    logging.info("{user}: success to get user info".format(user=user))
    print("{user}: success to get user info".format(user=user))
    return


def get_page(url,user):
    try:
        driver.get(url)
        driver.add_cookie(cookie_dict=cookie)
        driver.get(url)
        if driver.title == '豆瓣':
            logging.info("{user}: user cancel now".format(user=user))
            print("{user}: user cancel now".format(user=user))
            return
        elif driver.title == '该用户帐号状态异常':
            logging.info("{user}: user account status is abnormal".format(user=user))
            print("{user}: user account status is abnormal".format(user=user))
            return
        else:
            get_user_info(user)
    except:
        exceptionInfo()
        logging.info(">>>>>>>>>>>>>>>>>>>>> {user}: fail to get user info".format(user=user))
        print(">>>>>>>>>>>>>>>>>>>>>{user}: fail to get user info".format(user=user))
        return


if __name__ == "__main__":
    # 读文件得到users
    with open('user_bazu', 'r') as f:
        lines = f.readlines()
    users_list = eval(lines[0])

    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    logging.basicConfig(filename='user.log', level=logging.INFO, format=LOG_FORMAT)
    logging.info("Begin process")
    for user_id in users_list:
        logging.info("{user_id}: user_id begining".format(user_id=user_id))
        print("{user_id}: user_id begining".format(user_id=user_id))
        home = 'https://www.douban.com/people/' + str(user_id) + "/"
        get_page(home,user_id)
        logging.info("{user_id}: Complete and sleep to next user".format(user_id=user_id))
        print("{user_id}: Complete and sleep to next user".format(user_id=user_id))
        time.sleep(2 + random.randint(0, 3))

driver.quit()
