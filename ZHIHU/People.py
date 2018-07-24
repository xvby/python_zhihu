import os
import re
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
    # proxies=
    url ="https://www.zhihu.com/api/v4/members/"+sUserName+"/followees"
    return s.get(url,params=params, proxies=proxies)


def fetch_all_followee(sUrl):
    session = init(sUrl)
    sUserName = sUrl.split('/')[-2]
    offset = 0
    limit=20
    aFollowee=[]
    is_end=False
    proxy_db = db.Database( "HignAnnoProxy/ProxyPoolDB.db")
    https = proxy_db.fetch_one("https")
    http = proxy_db.fetch_one("http")
    proxies = {'http': str(http), 'https': str(https), }
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
    if eFollowee['gender'] == 1 and eFollowee['is_advertiser'] == False and eFollowee['user_type'] == 'people' and eFollowee['follower_count'] >= 500 :
       followee = {eFollowee['name'], eFollowee['url_token'], eFollowee['follower_count']}
       aList+=followee
    return aList

sUrl = 'https://www.zhihu.com/people/zhouxueyan/following'
aFollowee = fetch_all_followee(sUrl)
aFolloweeSelected = []
for followee in aFollowee:
    aFolloweeSelected = grab_followee_with_cond(followee, aFolloweeSelected)

print(aFolloweeSelected)