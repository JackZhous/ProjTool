#!/bin/bash
#!encoding=utf-8
import urllib2
import getopt
import thread
import threading
import sys
import re
import os

BASE_URL1 = ''
BASE_URL2 = ''

BILL_URL1 = ''
BILL_URL2 = 'o'

download_file = []
keywords = 'COM_MIN_OVER_PACK fCycleValidPower'
max_power = 200.0

#下载模块
def download(thread_name, url):
	print 'log file form %s is downloading...' % url
	print 'save the filename: %s' % thread_name
	f = urllib2.urlopen(url)
	data = f.read()
	with open(thread_name, "wb") as code:
		code.write(data)
		code.flush()
		download_file.append(thread_name)
		print '%s download success ' % thread_name

#初始化命令行参数
def init_opts(argv):
	try:
		opts, args = getopt.getopt(argv, 'hp:d:v:u:')
	except getopt.GetoptError:
		print 'Error: args input error'
		print '"-p xxx.txt" <is already download file>'
		print '"-d 2018-05-21" <the date you will download log> | or "today" means download toady log'
		print '"-v 200" <big than this power will be filter>'
		print '"-u b means bill base url"'
		sys.exit(2)
	return opts


def start_download(url):
	if url == 'today':
		url1 = BASE_URL1
		url2 = BASE_URL2
	else:
		url1 = BASE_URL1 +'_' + url + '.log'
		url2 = BASE_URL2 + '_' + url + '.log'
	try:
		t1 = threading.Thread(target=download, args=('%s_logs1.txt'%url, url1))
		t2 = threading.Thread(target=download, args=('%s_logs2.txt'%url, url2))
		t1.start()
		t2.start()
		t2.join()
		t1.join()
	except Exception, e:
		repr(e)

#分线程过滤
def filters(source_file, target_file, value):
	valueClass = value.isdigit()
	if valueClass:
		value = int(value)
	if os.path.exists(source_file):
		target = open(target_file, 'wb')
		lines = open(source_file)
		for line in lines:
			if valueClass:
				if keywords in line:
					lists = line.split(':')
					power = float(lists[len(lists)-1])
					if power >= value:
						target.write(line)
			else:
				if value in line:
					target.write(line)

#开始过滤任务
def start_filter(value):
	ths = []
	index = 0
	print '\nstart filter....'
	for f in download_file:
		t = threading.Thread(target=filters, args=(f, 'filter%d.txt'%index, value))
		t.start()
		index = index + 1
		ths.append(t)
	
	for th in ths:
		th.join()
	print 'finish filter'


def start_work(files, downloads,  value):
	print '--- task is start ---\n'
	if downloads is not None and downloads != '':
		start_download(downloads)
	if files is not None and files != '':
		download_file.append(files)
	if value > 0:
		start_filter( value)
	print '--- task is complete ---\n'

if __name__ == '__main__':
	opts = init_opts(sys.argv[1:])
	already_download = ''
	download_url = ''
	value = 0
	for opt, arg in opts:
		if opt == '-p':
			already_download = arg
		elif opt == '-d':
			download_url = arg
		elif opt == '-v':
			value = arg
		elif opt == '-u':
			url = str(arg)
			if url == 'b':
				BASE_URL1 = BILL_URL1
				BASE_URL2 = BILL_URL2
		else:
			print 'Error: args input error'
			print '"-p xxx.txt" <is already download file>'
			print '"-d 2018-05-21" <the date you will download log> | or "today" means download toady log'
			print '"-v 200" <big than this power will be filter> or string as keyword'
			print '"-u b means bill base url"'
			sys.exit()

	start_work(already_download, download_url,  value)
