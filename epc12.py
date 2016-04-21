#!/usr/bin/python  

from html.parser import HTMLParser
from urllib.parse import urlparse 
import urllib
import http.cookiejar 
import string 
import re 
from bs4 import BeautifulSoup
import sys
from pip._vendor.distlib.compat import raw_input
import time
import socket
import gl
import json
def epcPlay(opener,headers):        
    #打开登录主页面（他的目的是从页面下载cookie，这样我们在再送post数据时就有cookie了，否则发送不成功） 
    req = urllib.request.Request(hosturl, headers=headers)
    h = opener.open(req,timeout = 2)
    #print(h.read())
    h.close()
    data = getImag(hosturl,opener,headers)
    check = raw_input('Please enter the authcode:')
    #构造Post数据，他也是从抓大的包里分析得出的。 
    postData = {
                'submit_type' : 'user_login',
                'name' : '学号',
                'pass' : '你的密码',
                'txt_check' : check,
                'user_type':'2',
                'Submit': 'LOG IN'
                } 
    print(postData)
    #需要给Post数据编码 
    postData = urllib.parse.urlencode(postData) 
    #通过urllib2提供的request方法来向指定Url发送我们构造的数据，并完成登录过程 
    request = urllib.request.Request(posturl, postData.encode(encoding="utf-8",errors="ignore"), headers) 
    #print(request)
    response = opener.open(request) 
    text = response.read()
    response.close()
    soup = BeautifulSoup(text)
    #print(soup.prettify())
    #print(text)
    
    
def getImag(hosturl,opener,headers):
    imagrl = hosturl + "/" + "checkcode.asp"
    fileToSave = 'E:\\code.jpg'
    #必须模拟浏览器才能get到网页表
    req = urllib.request.Request(imagrl,headers=headers)
        
    operate = opener.open(req,timeout=2)
    data = operate.read()
    operate.close()
    if data == None:
        return
    file = open(fileToSave,'wb')
    file.write(data)
    file.flush()
    file.close()
    
def getWeek(opener):
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36', 
               'Referer' : 'http://epc.ustc.edu.cn/n_left.asp?base_id=2&second_id=0'} 
    #使用get方式时，请求数据直接放在url中。!!!!!!!!!!!!!!!!!!!!!
    oralurl = "http://epc.ustc.edu.cn/m_practice.asp?second_id=2002"
    
    #!!!!!注意此处如何使用headers
    request = urllib.request.Request(oralurl,headers=headers) 
    #print(request)
    response = opener.open(request) 
    text = response.read()
    response.close()
    data = text.decode('gb2312',errors="ignore")
    # outfile=open('e:/code.txt', 'wb')
    # outfile.write(text)
    # outfile.close()    
    soup = BeautifulSoup(text)
    tag = soup.find('form')
    s = re.search(r"week_day=\d+",tag['action'])
    gl.week_day = int(re.search(r"\d+",s.group(0)).group(0))
    s = re.search(r"week=\d+\d?",tag['action'])
    return int(re.search(r"\d+\d?",s.group(0)).group(0))
    
def getTable2002(opener,week):
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36', 
               'Referer' : 'http://epc.ustc.edu.cn/m_practice.asp?second_id=2002'} 
    rUrl = "http://epc.ustc.edu.cn/m_practice.asp?base_id=2&second_id=2002"
    #print(rUrl)
    try:
        request = urllib.request.Request(rUrl,headers=headers) 
        #print(request)
        response = opener.open(request) 
        text = response.read()
        response.close()
        data = text.decode('gb2312',errors="ignore")
        soup = BeautifulSoup(text, from_encoding="GB2312")
        timeC = re.compile(r'2016.+')
        print("second_id is 2002:")
        tag = soup.find_all('form')
        for list in tag:
            #print(list)
            timeC = re.compile(r'\d*:\d*-\d*:\d*')
            dayC = re.compile(r'周.+')
            teacherC = re.compile(r'[A-Z]+.+')
            patt = re.compile(r'第.?.?周')
            option = list.find("td",text = patt)
            s = re.search(r"\d+",option.text).group(0)
            ftime = list.find("br",text = timeC)
            fday = list.find("td",text = dayC)
            option1 = list.find("td",text = teacherC)
            fteacher = option1.find_next_sibling('td',text = teacherC)
            canOrder = re.compile(r'预约时间未到')
            option = list.find("input",{"value":"预 约"})
            #print(option['type'])
            print("week:" + s + fday.text + ftime.text + fteacher.text)
            if(int(s) == week) or (int(s) == week+1):
                action = re.sub(r'page=\d+','page=1',list['action'])
    except urllib.error.URLError as e:
        print(e.reason)
    except urllib.error.HTTPError as e:
        print(e.reason)
    return 0
        
def getTable2003(opener,week):
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36', 
               'Referer' : 'http://epc.ustc.edu.cn/m_practice.asp?second_id=2003'} 
    rUrl = "http://epc.ustc.edu.cn/m_practice.asp?base_id=2&second_id=2003"
    try:
        request = urllib.request.Request(rUrl,headers=headers) 
        #print(request)
        response = opener.open(request) 
        text = response.read()
        response.close()
        data = text.decode('gb2312',errors="ignore")
        soup = BeautifulSoup(text, from_encoding="GB2312")
        patt = re.compile(r'第.?.?周')
        print("second_id is 2003:")
        tag = soup.find_all('form')
        for list in tag:
            timeC = re.compile(r'\d*:\d*-\d*:\d*')
            dayC = re.compile(r'周.+')
            teacherC = re.compile(r'[A-Z]+.+')
            patt = re.compile(r'第.?.?周')
            option = list.find("td",text = patt)
            s = re.search(r"\d+",option.text).group(0)
            ftime = list.find("br",text = timeC)
            fday = list.find("td",text = dayC)
            option1 = list.find("td",text = teacherC)
            fteacher = option1.find_next_sibling('td',text = teacherC)
            #canOrder = re.compile(r'预约时间未到')
            option = list.find("input",{"value":"预 约"})
            #print(option['type'])
            print("week:" + s + fday.text + ftime.text + fteacher.text)
            if(int(s) == week) or (int(s) == week+1):
                action = re.sub(r'page=\d+','page=1',list['action'])
    except urllib.error.URLError as e:
        print(e.reason)
    except urllib.error.HTTPError as e:
        print(e.reason)
    return 0
    
def getTable2004(opener,week):
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36', 
               'Referer' : 'http://epc.ustc.edu.cn/m_practice.asp?second_id=2004'} 
    rUrl = "http://epc.ustc.edu.cn/m_practice.asp?base_id=2&second_id=2004"
    try:
        request = urllib.request.Request(rUrl,headers=headers) 
        #print(request)
        response = opener.open(request) 
        text = response.read()
        response.close()
        data = text.decode('gb2312',errors="ignore")
        soup = BeautifulSoup(text, from_encoding="GB2312")
        patt = re.compile(r'第.?周')
        print("second_id is 2004:")
        tag = soup.find_all('form')
        for list in tag:
            timeC = re.compile(r'\d*:\d*-\d*:\d*')
            dayC = re.compile(r'周.+')
            teacherC = re.compile(r'[A-Z]+.+')
            patt = re.compile(r'第.?.?周')
            option = list.find("td",text = patt)
            s = re.search(r"\d+",option.text).group(0)
            ftime = list.find("br",text = timeC)
            fday = list.find("td",text = dayC)
            option1 = list.find("td",text = teacherC)
            fteacher = option1.find_next_sibling('td',text = teacherC)
            canOrder = re.compile(r'预约时间未到')
            option = list.find("input",{"value":"预 约"})
            #print(option['type'])
            print("week:" + s + fday.text + ftime.text + fteacher.text)
            if(int(s) == week) or (int(s) == week+1):
                # if(option['type'] == 'submit'):
                    # continue
            # if(int(s) == week):
                # if(checkIfForbid(fday.text,ftime.text)==1):  
                    # if(fteacher.text == 'Hanna'):
                action = re.sub(r'page=\d+','page=1',list['action'])
    except urllib.error.URLError as e:
        print(e.reason)
    except urllib.error.HTTPError as e:
        print(e.reason)
    return 0
    
def postTable(opener,week,second_id,action):
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36', 
               'Referer' : 'http://epc.ustc.edu.cn/m_practice.asp?second_id=' + str(second_id),
                           
                'Accept' :'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'zh-CN,zh;q=0.8',
                'Accept-Encoding': 'gzip, deflate',
                'Host':    'epc.ustc.edu.cn',
                'Connection':'keep-alive',
                'Upgrade-Insecure-Requests':'1',
                'Origin':'http://epc.ustc.edu.cn'} 
    postUrl = "http://epc.ustc.edu.cn" + "/" + action
    
    print(compose_debug_url(postUrl))
    postData = {
                'submit_type': 'book_submit'
                } 
    print(postData)
    #需要给Post数据编码 
    postData = urllib.parse.urlencode(postData) 
    #通过urllib2提供的request方法来向指定Url发送我们构造的数据，并完成登录过程 
    request = urllib.request.Request(compose_debug_url(postUrl), postData.encode(encoding="utf-8",errors="ignore"),headers) 
    #print(request)
    try:
        response = opener.open(request)
    except urllib.error.URLError as e:
        print(e.reason)
    except urllib.error.HTTPError as e:
        print(e.reason)
    text = response.read() 
    response.close()
    outfile=open('e:/code.txt', 'wb')
    outfile.write(text)
    outfile.close()
    soup = BeautifulSoup(text)
    postToSAE(opener,'1','0',action)
    #print(soup.prettify())
    #print(text)

def compose_debug_url(input_url):
    input_url_parts = urllib.parse.urlsplit(input_url)
    input_query = input_url_parts.query
    input_query_dict = urllib.parse.parse_qs(input_query)

    modified_query_dict = dict(urllib.parse.parse_qsl(input_query) + [('submit_type', 'book_submit')])
    modified_query = urllib.parse.urlencode(modified_query_dict)
    modified_url_parts = (
      input_url_parts.scheme,
      input_url_parts.netloc,
      input_url_parts.path,
      modified_query,
      input_url_parts.fragment
    )

    modified_url = urllib.parse.urlunsplit(modified_url_parts)

    return modified_url
    
    
def checkIfForbid(week_day,time):
    js = json.dumps(gl.forbidList)
    #print(js)
    jss = json.loads(js)
    for obj in jss['forbid']:
        #print(obj['week_day'])
        if (obj['week_day'] == week_day) and (obj['time'] == time):
            return 0
    return 1
flag = 0
sleep_download_time = 20 
#time.sleep(sleep_download_time) #这里时间自己设定     
#构造header，一般header至少要包含一下两项。这两项是从抓到的包里分析得出的。 
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36', 
               'Referer' : 'http://epc.ustc.edu.cn/n_left.asp'} 
#登录的主页面 
hosturl = 'http://epc.ustc.edu.cn'
#post数据接收和处理的页面（我们要向这个页面发送我们构造的Post数据） 
posturl = 'http://epc.ustc.edu.cn/n_left.asp'
#设置一个cookie处理器，它负责从服务器下载cookie到本地，并且在发送请求时带上本地的cookie 
cj = http.cookiejar.CookieJar() 
cookie_support = urllib.request.HTTPCookieProcessor(cj) 
opener = urllib.request.build_opener(cookie_support) 
urllib.request.install_opener(opener) 
epcPlay(opener,headers)
gl.week = getWeek(opener)
while(flag != 2):
    #time.sleep(10)
    flag = getTable2002(opener,gl.week)
    if(flag == 1): break
    time.sleep(sleep_download_time) #这里时间自己设定     
    flag = getTable2003(opener,gl.week)
    if(flag == 1): break
    time.sleep(sleep_download_time) #这里时间自己设定     
    flag = getTable2004(opener,gl.week)
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))