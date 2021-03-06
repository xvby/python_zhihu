import os
import re
import xlwt
import xlrd
from xlutils.copy import copy
import ctypes
import requests


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


def fetch_all_followee(sUrl,):
    session = init(sUrl)
    sUserName = sUrl.split('/')[-2]
    offset = 0
    limit=20
    aFollowee=[]
    is_end=False
    # proxy_db = db.Database( "HignAnnoProxy/ProxyPoolDB.db")
    # https = proxy_db.fetch_one("https")
    # # http = proxy_db.fetch_one("http")
    while not is_end:
        try:
            ret=fetch_followee(session,sUserName,limit,offset,proxies)
        #total = ret.json()['paging']['totals']
            aFollowee+=ret.json()['data']
        except:
            print("Proxy Error:", proxy)
            instanceProxy.delete_proxy(proxy)
            proxy = instanceProxy.get_proxy()
            proxies = {"https": proxy}
            continue
        is_end= ret.json()['paging']['is_end']
        print("Offset: ",offset)
        print("is_end: ",is_end)
        print("Proxy:", proxy)
        offset+=limit
    return aFollowee

def grab_followee_with_cond(eFollowee, aList):
    if eFollowee['is_advertiser'] == False and eFollowee['user_type'] == 'people' :
       people = { 'name' : eFollowee['name'], 'gender': eFollowee['gender'], 'url': eFollowee['url_token'], 'followee' : eFollowee['follower_count'] }
       aList.append(people)
    return aList

def output(filename, sheet, list):
    #save the file for copy first
    try:
        os.remove(filename + '_copy.xls')
    except:
        print("no copy file exists")
    try:
        rb = xlrd.open_workbook(filename + '.xls', on_demand = True )
    except:
        print("no original file exists")
    else:
        wbcopy = copy(rb)
        wbcopy.save(filename + '_copy.xls')
        rb.release_resources()
        del rb
        #delete the original file
        os.remove(filename + '.xls')
    #generating new file
    wb = xlwt.Workbook()
    ws = wb.add_sheet(sheet)
    i = 0
    for elem in list:
        ws.write(i, 0, elem['name'])
        ws.write(i, 1, elem['gender'])
        ws.write(i, 2, elem['url'])
        ws.write(i, 3, elem['followee'])
        i+=1
    wb.save( filename + '.xls' )

def read(filename, sheet_index):
    book = xlrd.open_workbook(filename + '.xls')
    sheet = book.sheet_by_index(sheet_index)
    aList = []
    for row_index in range(sheet.nrows):
        row_data = sheet.row_values(row_index)
        data = {'name' : row_data[0], 'gender' : row_data[1], 'url' : row_data[2], 'followee': row_data[3]}
        aList.append(data)
    return aList

class Proxy:
    index = 0
    aProxy = []

    def __init__(self, bSAP):
        if bSAP == 'true':
           Proxy.sap_proxy()
        else:
           Proxy.other_proxy()

    def get_proxy(self):
        Proxy.index += 1
        return Proxy.aProxy[(Proxy.index % len(Proxy.aProxy))]


    def delete_proxy(self, proxy):
        x = Proxy.aProxy.index(proxy)
        Proxy.aProxy[x:x + 1] = []

    @staticmethod
    def other_proxy():
        from HignAnnoProxy import db
        db = db.Database(LOCATION="HignAnnoProxy")
        Proxy.aProxy = db.get_proxy_addr()

    @staticmethod
    def sap_proxy():
        Proxy.aProxy = ["http://proxy.syd.sap.corp:8080",
                  "http://proxy.igb.sap.corp:8080",
                  "http://proxy.phl.sap.corp:8080",
                  "http://proxy.pal.sap.corp:8080",
                  # "http://proxy.lax.sap.corp:8080",
                  "http://proxy.chi.sap.corp:8080",
                  "http://proxy.nyc.sap.corp:8080",
                  "http://proxy.sel.sap.corp:8080",
                  "http://proxy.tyo.sap.corp:8080",
                  "http://proxy.sha.sap.corp:8080",
                  "http://proxy.pvgl.sap.corp:8080",
                  "http://proxy.hkg.sap.corp:8080",
                  "http://proxy.lon.sap.corp:8080",
                  "http://proxy.par.sap.corp:8080",
                  "http://proxy.sin.sap.corp:8080",
                  "http://proxy.syd.sap.corp:8080",
                  "http://proxy.blr.sap.corp:8080",
                  "http://proxy.blrl.sap.corp:8080",
                  "http://proxy.jnb.sap.corp:8080"]



####################### main functionality ######################

# bInit = input("Init(y/n)?: ")
# while 1 == 1:
    # bInit = ctypes.windll.user32.MessageBoxW(0, "Init without excel file exists?", "Message", 4)
    bInit = 0
    aPending = []
    aResult = []

    if bInit == 6:
        start = { 'name' : '', 'gender' : '', 'url' : 'zhouxueyan', 'followee': '' }
        aPending.append(start)
    else:
        aPending = read('pending',0)
        aResult = read('Result',0)

    # bSAP = ctypes.windll.user32.MessageBoxW(0, "Proxy using SAP", "Message", 4)
    # bSAP = 0
    # if bSAP == 6:
    #     Proxy.bSAP = 'true'
    # else:
    #     Proxy.bSAP = 'false'
    instanceProxy = Proxy(bSAP="false")
    proxy = instanceProxy.get_proxy()
    proxies = {"https": proxy}

    for people in aPending:
        if people in aResult:
            continue
        sUrl = 'https://www.zhihu.com/people/' + people['url'] + '/following'
        aFollowee = fetch_all_followee(sUrl)
        aFolloweeFiltered = []
        for followee in aFollowee:
            aFolloweeFiltered = grab_followee_with_cond(followee, aFolloweeFiltered)
        aPending.extend(aFolloweeFiltered)

        # add people from Pending to Result
        aResult.append(people)
        aPending.remove(people)

        # Output to excel
        # if len(aResult) % 10 == 0:
            # bContinue = ctypes.windll.user32.MessageBoxW(0, "Continue to catch the data", "Message", 4)
            # if bContinue == 7 :
        output("Result","sheet1",aResult)
        output("pending","sheet1",aPending)
            # break


