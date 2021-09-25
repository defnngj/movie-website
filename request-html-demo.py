"""
author: bugmaster
data: 2021-09-25
function: 爬取 豆瓣 top250 电影信息
"""
import sqlite3
from requests_html import HTMLSession
session = HTMLSession()


def save_db(name, img_url, grade, number):
    """
    保存数据库
    """
    conn = sqlite3.connect('move.db')
    print(conn)
    c = conn.cursor()
    c.execute(f"""INSERT INTO move (name,img,grade,number) 
          VALUES ('{name}', '{img_url}', {grade}, {number} )""")
    conn.commit()
    conn.close()


# 0 25 50 75 ... 225
for page in range(0, 250, 25):  # 10页
    print(f'https://movie.douban.com/top250?start={page}&filter=')
    r = session.get(f'https://movie.douban.com/top250?start={page}&filter=')
    imgs = r.html.find('a > img')
    stars = r.html.find('.rating_num')
    evaluates = r.html.find('.star > span:nth-child(4)')
    for i in range(25):
        print(i)
        # print(imgs[i].attrs)
        # print(stars[i].text)
        # print(evaluates[i].text)
        name = imgs[i].attrs["alt"]
        img = imgs[i].attrs["src"]
        grade = stars[i].text
        number = int(evaluates[i].text[0:-3])
        print(name)
        print(img)
        print(grade)
        print(number)
        save_db(name, img, grade, number)










