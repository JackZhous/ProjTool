#!/bash/bin
#encoding=utf-8


from openpyxl import *
da = {u'\u4e00\u751f\u53ea\u4e3a\u4f60': 3, u'\u574f\u5b69\u5b50\xb9\xb9\xb9\u2074\u2082\u2080\u2081\u2086': 4, u'\u53ef\u7231\u7684\u4f60': 3, u'Ms  G': 3, u'\u674e\u80dc\u9e3f': 2}
tt = ''
for ii in da:
	tt =  ii

test = str(da).encode('utf-8')
book = Workbook()
sheet0 = book.create_sheet(u'异常详细表格', 0)
sheet0.append([tt, test])
book.save('mmm.xlsx')

