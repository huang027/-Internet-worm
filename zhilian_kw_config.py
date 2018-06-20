import requests
from urllib.parse import urlencode
from bs4 import BeautifulSoup
import pandas as pd
from requests.exceptions import RequestException
from tqdm import tqdm


def get_one_page(city,keyword,page):
    paras = {
        'jl': city,
        'kw': keyword, #比如成都：https://sou.zhaopin.com/jobs/searchresult.ashx?jl=c成都&kw=python&p=1&isadv=0，换关键词python为python,kw=python,第一页p=1
        'p': page,  # 页数，如果还要加上城市的话，可以写'j1':city
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'}
    url = 'http://sou.zhaopin.com/jobs/searchresult.ashx?'  + urlencode(paras)
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:# 200表示请求成功，303表示重定向，400表示请求错误，401表示未授权，403表示禁止访问，404表示文件未找到，500表示服务器错误
            return response.text
        return None
    except RequestException as e:
        return None

def parse_one_page(html):
    soup=BeautifulSoup(html,'lxml')
    body=soup.body
    date_main=body.find('div',{'class':'newlist_list_content'})
    if date_main:
        tables=date_main.find_all('table')
        for i,table_info in enumerate(tables):
            if i ==0:  #如果第一个table 是抓取的内容，则该代码可以省去
                continue
            tds = table_info.find('tr').find_all('td')
            zwmc = tds[0].find('a').get_text()  # 职位名称
            zw_link = tds[0].find('a').get('href')  # 职位链接
            fkl = tds[1].find('span').get_text()  # 反馈率
            gsmc = tds[2].find('a').get_text()  # 公司名称
            zwyx = tds[3].get_text()  # 职位月薪
            gzdd = tds[4].get_text()  # 工作地点
            gbsj = tds[5].find('span').get_text()  # 发布日期
            tr_brief = table_info.find('tr', {'class': 'newlist_tr_detail'})
            # 招聘简介
            brief = tr_brief.find('li', {'class': 'newlist_deatil_last'}).get_text()
            # 用生成器获取信息
            yield {'zwmc': zwmc,  # 职位名称
                   'fkl': fkl,  # 反馈率
                   'gsmc': gsmc,  # 公司名称
                   'zwyx': zwyx,  # 职位月薪
                   'gzdd': gzdd,  # 工作地点
                   'gbsj': gbsj,  # 公布时间
                   'brief': brief,  # 招聘简介
                   'zw_link': zw_link,  # 网页链接
                   }


def main(city,keyword,pages):
    jobs = []
    for i in tqdm(range(pages)):
        html = get_one_page(city,keyword,i)
        items = parse_one_page(html)
        for item in items:
            jobs.append(item)
    jobs=pd.DataFrame(jobs)
    jobs.to_csv('G:\data\jobs.csv')

if __name__ == '__main__':
    main('武汉','python',10)





