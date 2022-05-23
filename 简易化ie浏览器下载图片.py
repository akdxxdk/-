# -*- coding: utf-8 -*-
# @Author  : KongDeXing
# @Time    : 2022/1/7 9:08
# @Function: Data_Analysis
import random
from requests_html import HTMLSession, HTML, AsyncHTMLSession

class BenXiTest:
    def __init__(self, url):
        self.start_url = url
        self.session = HTMLSession()  # 实例化session
        self.aSession = AsyncHTMLSession()  # 实例化异步session
        users = {  # 可以在发送请求的时候更换user-agent
            1: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0',
            2: 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
            3: 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
            4: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
            5: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
        }
        ur1 = random.sample(users.keys(), 1)
        self.headers = "users" + str(ur1)

    def get_response(self):
        """获取响应，并返回requests_html中的HTML对象"""
        start_url = self.start_url
        r = self.session.get(start_url, headers={'user-agent': self.headers})
        print("网页状态", r)
        return r.html

    # 清洗数据（提取数据）
    def get_data(self):
        """使用xpath获取数据"""
        html = self.get_response()
        picture_Element = html.find("div  img")

        picture_url_list = []
        for i in picture_Element:
            attrs = i.attrs
            pic_list1 = str(attrs.get("src"))
            pic_list2 = str(attrs.get('data-src'))
            if "https://" in pic_list1:
                picture_url_list.append(pic_list1)
            if "https://" in pic_list2:
                picture_url_list.append(pic_list2)
        return picture_url_list

    def download_picture(self,picture_url_list):
        pic_path = input("请输入保存路径：")
        count = 0
        for url in picture_url_list:
            r = self.session.get(url, headers={'user-agent': self.headers})
            print("网页状态", r)
            data =  r.content
            with open(pic_path+str(count)+".png","wb") as f:
                f.write(data)
            count += 1
        print("图片保存成功！！")

if __name__ == '__main__':
    关键词 = input("请输入搜索关键词：")
    url = "https://cn.bing.com/images/search?q="+关键词+"&form=HDRSC2&first=1&tsc=ImageBasicHover"
    test = BenXiTest(url)
    pinture_url_list = test.get_data()
    test.download_picture(pinture_url_list)
