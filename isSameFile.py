#!/bin/bash
#encoding=utf-8

# 判断两个文件是否相同根据其md5值

import hashlib
import sys
import os

def main(file1_path, file2_path):
	result = 'false'
	if os.path.isfile(file1_path) or os.path.isfile(file2_path):
		file1 = readFileContent(file1_path)
		file2 = readFileContent(file2_path)
		file1_md5 = md5_string(file1)
		file2_md5 = md5_string(file2)
		if file1_md5 == file2_md5:
			result = 'true'
	else:
		result = 'path error'
	print result

def readFileContent(path):
	f = open(path)
	content = f.read()
	return content

def md5_string(str_data):
	m = hashlib.md5()
	m.update(str_data)
	code = m.hexdigest()
	return code


if __name__ == '__main__':
	main(sys.argv[1], sys.argv[2])
