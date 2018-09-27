#!/bin/bash
#ecoding=utf-8
# author: jackzhous
# 描述：基础类，直接爬网站爬下来的原始数据
import sys
import urllib2
import json
import imageio
import hashlib
import cookielib

host_chongqing2 = ''
host_hechi = ''
user_chongqing2 = ''
user_hechi = ''

class EasyCharger:
	type = {'Content-Type': 'application/json', 'Token':'null'}
	def __init__(self, output_file_name):
		self.host = host_chongqing2
		self.user = user_chongqing2
		self.filename = output_file_name
		self.token = 'null'
		self.passwd = 'zywlw_cd'
		self.cookie = cookielib.CookieJar()
                self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookie))

	#更新服务器地址1-chongqing2  2-hechi
	def update_net(self, server_flag):
		if 1 == server_flag:
			self.host = host_chongqing2
			self.user = user_chongqing2
		else:
			self.host = host_hechi
			self.user = user_hechi
	
	# 登录
	def login(self, code):
		url = self.host + 'login'
		data = {"mobile":self.user}
		data.setdefault('password',self.md5_str())
		data.setdefault('code', code)
		result = self.network(url, data)
		try:
			str_token = result["token"]
			#self.token = str_token
			self.token = ''
			self.type['Token'] = str_token
			return 'true' 
		except KeyError as ke:
			print result
			return '登录失败，请刷新验证码重新开始分析'

	# 登录的图片验证码
	def validation(self):
		url = self.host + 'validation'
		result = self.network(url, None)
		image = open('t.png', 'wb')
		image.write(result)
		image.close()
		self.convertPNGtoGif()	

	# 将png图片转换为gif
	def convertPNGtoGif(self):
		images = []
		images.append(imageio.imread('t.png'))
		imageio.mimsave('t.gif', images, duration = 1)


	# 所有充电站的总表
	def listAllProvinceData(self):
		url = self.host + 'device/selectStaion'
		data = {"currentPage":1,"itemsPerPage":10}
		result = self.network(url, data)
		ret = self.checkResponse(result)
		if ret == "true":
			data["itemsPerPage"] = result["total"]
			result = self.network(url, data)
			ret = self.checkResponse(result)
			if ret == "true":
				return result["rows"]
		return ret

	# 搜索某个充电桩
	def searchStation(self, stationName):
		url = self.host + 'device/selectStaion'
		data = {"currentPage":1,"itemsPerPage":10, 'statag':stationName}
		result = self.network(url, data)
		ret = self.checkResponse(result)
		if ret == "true":
			return result['rows']

	# 检测网络返回值
	def checkResponse(self, result):
		try:
			if result["code"] == 1:
				return "true"
			return "false"
		except:
			print result
			return 'false'
		
	# 每个充电站的具体信息 staid充电站id count 总共的条数
	def findPortPerStation(self, staid, count):
		url = self.host + 'plug/selectDevice'
		data = {"currentPage":1,"itemsPerPage":count, "devtype":2, "pestaid":staid}
		result = self.network(url, data)
		ret =  self.checkResponse(result)
		if ret == "true":
			return result["rows"]
		return ret
				
	# 查看每个电站的网关
	def findGateway(self, staid):
		url = self.host + 'device/selectGateway'
		data = {"currentPage":1,"itemsPerPage":100, "devtype":1, "devstaid":staid}
		result = self.network(url, data)
		ret =  self.checkResponse(result)
		if ret == "true":
			return result["rows"]
		return ret	
		

	#网络访问部分
	def network(self, url, data):
		ret = {}
		try:
			if data is not None:
				jdata = json.dumps(data)
				request = urllib2.Request(url, jdata, self.type)
				response = self.opener.open(request)
				ret = json.loads(response.read())
			else:
				request = urllib2.Request(url)
				response = self.opener.open(request)
				ret =  response.read()
		except Exception, e:
			print 'network error %s' % str(e)
		return ret
			
	
	#过滤每个充电站中有异常端口的数据，只返回不正常的数据
	def filiterLostStatusData(self, ports):
		lostStatusPorts = []
		for port in ports:
			status = port['pgstatus']
			if status == 10 or status == 2:	#异常状态
				per = {"pgstatus":status, "pgnum":port["pgnum"]}
				lostStatusPorts.append(per)
		return lostStatusPorts
	
	#查询设备的告警日志
	# 请求数据格式
	#{
	#	"deviceImei": "5149013215964394",
	#	"startTime": "2018-03-06",
	#	"endTime": "2018-03-27",
	#	"currentPage": 1,
	#	"itemsPerPage": 10
	#}	
	def getAlarm(self, station):
		url = self.host + "alarm/listAlarm"
		result = self.network(url, station)
		if result is not None:
			return result
		return "false"

	def getProvinceInfo(self):
		url = self.host + "common/provinces"
		data = {}
		result = self.network(url, data)
		if result is not None:
			province = result['provinces']
			p_dic = {}
			for item in province:
				p_dic.setdefault(item['id'], {'name':item['name']})
			return p_dic
		return 'false'
	def md5_str(self):
		m = hashlib.md5()
		m.update(self.passwd)
		code = m.hexdigest()
		return code
	#添加白名单
	def add_device_data(self, device):
		url = self.host + "device/addActivation"
		result = self.network(url, device)
		if result['code'] != 1:
			print result.encode('utf-8')
			return result
		else:
			return 1
	#获取站点的阈值配置信息
	def getStationConfig(self, staId):
		url = self.host + 'device/getDeviceConfig'
		data = {'id': staId}
		result = self.network(url,data)
		return result

	def getStationOrder(self, staName, startTime, endTime):
		url = self.host + 'bill/search'
		data = {"stationType": 0,"billTypes": 2,"endTime": endTime,"startTime": startTime,"tag": staName,"currentPage": 1,"itemsPerPage": 1}
		result = self.network(url, data)
		if result['code'] != 1:
			return 'false'
		data['itemsPerPage'] = result['total']
		result = self.network(url, data)
		if result['code'] == 1:
			return result['rows']
		return 'false'


if __name__ == '__main__':
	charger = EasyCharger('xxx')
	charger.md5_str('zywlw_cd')
	print ret
