import os
import re
import xlwt
import requests

from ZHIHU.HignAnnoProxy import db

def init(url):
    ua = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
    s = requests.Session()
    s.headers.update(ua)
    ret=s.get(url)
    s.headers.update({"authorization":"oauth c3cef7c66a1843f8b3a9e6a1e3160e20"})
    return s

def fetch_followee(s,sUserName,iLimit,iOffset,proxies):
    params={
        'sort_by':'default',
        'include':'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics',
        'limit':iLimit,
        'offset':iOffset
    }
    # proxies=xlwt
    url ="https://www.zhihu.com/api/v4/members/"+sUserName+"/followees"
    return s.get(url,params=params,proxies=proxies)


def fetch_all_followee(sUrl):
    session = init(sUrl)
    sUserName = sUrl.split('/')[-2]
    offset = 0
    limit=20
    aFollowee=[]
    is_end=False
    # proxy_db = db.Database( "HignAnnoProxy/ProxyPoolDB.db")
    # https = proxy_db.fetch_one("https")
    # http = proxy_db.fetch_one("http")
    proxies = {"http": "http://proxy.syd.sap.corp:8080", "https": "http://proxy.syd.sap.corp:8080" }
    while not is_end:
        ret=fetch_followee(session,sUserName,limit,offset,proxies)
        #total = ret.json()['paging']['totals']
        aFollowee+=ret.json()['data']
        is_end= ret.json()['paging']['is_end']
        print("Offset: ",offset)
        print("is_end: ",is_end)
        offset+=limit
    return aFollowee


def grab_followee_with_cond(eFollowee, aList):
    if eFollowee['gender'] == 1 and eFollowee['is_advertiser'] == False and eFollowee['user_type'] == 'people' :
       people = { 'name' : eFollowee['name'], 'url': eFollowee['url_token'], 'followee' : eFollowee['follower_count'] }
       aList.append(people)
    return aList

def output(filename, sheet, list):

    wb = xlwt.Workbook()
    ws = wb.add_sheet(sheet)
    i = 0
    for elem in list:
        ws.write(i, 0, elem['name'])
        ws.write(i, 1, elem['url'])
        ws.write(i, 2, elem['followee'])
        i+=1

    wb.save(filename)


start = { 'name' : 'zhouxueyan', 'url' : 'zhouxueyan', 'followee' : 0 }
aPeople = []
aPeople.append(start)

aResult = []

for people in aPeople:
    sUrl = 'https://www.zhihu.com/people/' + people['url'] + '/following'
    aFollowee = fetch_all_followee(sUrl)
    aFolloweeSelected = []
    for followee in aFollowee:
        aFolloweeSelected = grab_followee_with_cond(followee, aFolloweeSelected)
    aPeople.extend(aFolloweeSelected)
    aResult.append(people)
    aPeople.remove(people)
    if ( len(aResult) ) % 10 :
        bContinue = input("Continue(y/n)?: ")
        if bContinue == "n" :
            output("Result.xls","sheet1",aResult)
            output("pending.xls","sheet1",aPeople)
            break


