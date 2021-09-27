"""
author: bugmaster
data: 2021-09-25
function: 爬取 豆瓣 top250 电影信息
"""
import os
import sqlite3
from requests_html import HTMLSession
session = HTMLSession()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(BASE_DIR, "static", "images")


def save_db(name, img_url, grade, number):
    """
    保存数据库
    """
    conn = sqlite3.connect('dev.db')
    print(conn)
    c = conn.cursor()
    c.execute(f"""INSERT INTO movie (name,img,grade,number) 
          VALUES ('{name}', '{img_url}', {grade}, {number} )""")
    conn.commit()
    conn.close()


def download_img(img_path, img_name):
    """
    保存图片
    :param img_path:
    :param img_name:
    :return:
    """
    try:
        req_pic = session.get(img_path)
        save_pic = os.path.join(IMG_DIR, img_name)
        with open(save_pic, "wb") as fp:
            fp.write(req_pic.content)
    except Exception as msg:
        print("下载中出现异常:%s" % str(msg))


def get_top_250():
    """
    获取电影：top250
    """
    for page in range(0, 250, 25):  # 10页
        print(f'https://movie.douban.com/top250?start={page}&filter=')
        r = session.get(f'https://movie.douban.com/top250?start={page}&filter=')
        imgs = r.html.find('a > img')
        stars = r.html.find('.rating_num')
        evaluates = r.html.find('.star > span:nth-child(4)')
        for i in range(25):
            name = imgs[i].attrs["alt"]
            img_path = imgs[i].attrs["src"]
            grade = stars[i].text
            number = int(evaluates[i].text[0:-3])
            # print(name)
            # print(img_path)
            # print(grade)
            # print(number)
            img_name = img_path.split("/")[-1]
            download_img(img_path, img_name)
            save_db(name, img_name, grade, number)


if __name__ == '__main__':
    get_top_250()





