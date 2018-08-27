# # a = input("Continue(y/n)?: ")
# # # if a == "y":
# # #     print("Yes")
# # # else:
# # #     print("No")
#
# import xlwt
# from datetime import datetime
#
# def output(filename, sheet, list):
#
#     wb = xlwt.Workbook()
#     ws = wb.add_sheet(sheet)
#     i = 0
#     for elem in list:
#         ws.write(i, 0, elem['name'])
#         ws.write(i, 1, elem['url'])
#         ws.write(i, 2, elem['followee'])
#         i+=1
#
#     wb.save(filename)
#
# start = { 'name' : 'zhouxueyan', 'url' : 'zhouxueyan', 'followee' : 0 }
# aPeople = []
# aPeople.append(start)
# output("text.xls","sheet1", aPeople)

# from HignAnnoProxy import db
# # db = db.Database(LOCATION = "HignAnnoProxy")
# #
# # a = db.fetch_all()
# # for i in a:
# # 	print(i[0])
# # 	print(i[1])
# # 	print(i[2])
index = 0
aProxy = ["http://proxy.syd.sap.corp:8080",
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
index += 1

print(aProxy[(index % len(aProxy))])