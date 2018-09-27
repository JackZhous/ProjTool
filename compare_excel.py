#!/bin/bash
#encoding=utf-8

#对比两个结构相同的excel表格  得出数据中新增、不变、和减少的

import os
import xlrd

class CompareEXCEL:
	def __init__(self, oldfile):
		self.oldF = oldfile
		self.unslove = 0
		self.add = 0
		self.sub = 0
		self.init_old_excel()

	#比较函数  新增的add+1并且返回add字符串
	def startCompare(self, target):
		try:
			key = self.dic[target]
		except KeyError:
			self.add = self.add + 1
			return 'add'
		else:
			self.unslove = self.unslove + 1
			return 'unslove'

	def init_old_excel(self):
		if os.path.isfile(self.oldF):
			wb = xlrd.open_workbook(self.oldF)
			sheets = wb.sheets()	#获取所有表格的名字
			sheet0 = sheets[0]			#获取第一个表格
			rows = sheet0.nrows
			dic = {}
			for row in range(rows):
				if row < 3:
					continue
				dic[sheet0.cell(row,2).value] = '1'
			if len(dic) < 1:
				print('没有旧数据')
				return
			self.dic = dic
		else:
			print('error')


	def init_bai_ming_dan_excel(self):
		file = self.oldF
		if file.endswith('.xls') and os.path.isfile(file):
			wb = xlrd.open_workbook(self.oldF)
			sheets = wb.sheets()	#获取所有表格的名字
			sheet0 = sheets[0]			#获取第一个表格
			rows = sheet0.nrows
			key0 = sheet0.cell(0,0).value
			key1 = sheet0.cell(0,1).value
			key2 = sheet0.cell(0,2).value
			key3 = sheet0.cell(0,3).value
			data = {}
			data['rows'] = []
			rows = rows - 1
			for row in range(rows):
				row_data = {}
				row_data[key0] = sheet0.cell(row+1,0).value
				row_data[key1] = sheet0.cell(row+1,1).value
				row_data[key2] = sheet0.cell(row+1,2).value
				row_data[key3] = sheet0.cell(row+1,3).value
				data['rows'].append(row_data)
			return data
		else:
			return 'false'

	def getAdd(self):
		return self.add

	def getSub(self):
		return (len(self.dic) - self.unslove)

	def getUnslove(self):
		return self.unslove
