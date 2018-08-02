# a = input("Continue(y/n)?: ")
# # if a == "y":
# #     print("Yes")
# # else:
# #     print("No")

import xlwt
from datetime import datetime

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
output("text.xls","sheet1", aPeople)