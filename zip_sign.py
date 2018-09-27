#!/bin/bash
#encoding=utf-8

import sys
import os
import re
from process import MyProcess


#修改assets/sdkParams文件的debug模式，只需要输入
def zip_sign(apk_path, apk_name):
	print(apk_path)
	if not os.path.exists(apk_path):
		print("the path is not exists ")
		return
	process = MyProcess('zip_sign')
	result = process.apktool_b(apk_path)
	if result == True:
		apk_out_file = apk_path+'/dist/' +apk_name
		result1 = process.exec_sign_apk(apk_out_file)
		if result1 == True:
			print("all success")
		else:
			print('sign error')
	else:
		print("zip file failed")

	
if __name__ == '__main__':
	zip_sign(sys.argv[1], sys.argv[2])
