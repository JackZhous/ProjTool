#!/bin/bash
#encoding=utf-8

from openpyxl import *
import json
from urllib import quote
import urllib2
import sys

host = ""

def main(token):
	if token is None or token == "":
		return
	depts = getAllDepts(token)
	personInfo = getPersonInfoPerDepts(token, depts)
	saveToXls(personInfo)

#获取所有的组织架构
def getAllDepts(token):
	url = host + '/portal/contacts/index/contactsTree'
	value = network(url, token)
	depts = []
	for i in range(len(value)):
		item = value[i]
		dept = {"id":item['deptName'], "deptNum":item['deptNum']}
		depts.append(dept)
	return depts

#获取每个组织下面的人员信息
def getPersonInfoPerDepts(token, depts):
	result = []
	url = '/portal/contacts/index/userList?deptName='
	for i in range(len(depts)):
		dept = depts[i]
		if dept['deptNum'] == 0:
			continue
		str = dept['id'].encode('utf-8')
		deptNameEncode = quote(str)
		perurl = host + url + deptNameEncode
		value = network(perurl, token)
		data = {"name":str, "person":value}
		result.append(data)
	return result

#网络络访问部分
def network(url, header):
	request = urllib2.Request(url)
	request.add_header('Cookie', header)
	response = urllib2.urlopen(request)
	value = json.loads(response.read())
	print value
	value = value['data']
	return value

#保存数据
def saveToXls(personInfo):
	book = Workbook()
	sheet0 = book.create_sheet(u'人员信息表', 0)
	sheet0.append(['部门组织', '姓名', '职称','电话','工号', '邮箱'])
	for persons in personInfo:
		deptName = persons['name']
		for person in persons['person']:
			data = [deptName, person['commonName'], person['position'], person['mobilePhoneNumber'], person['employeeId'], person['email']]
			sheet0.append(data)
	book.save('persons.xls')

# 参数要通过抓包工具抓到登录用户的token在填写进来
if __name__ == '__main__':
	main(sys.argv[1])
