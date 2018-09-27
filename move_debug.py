#!/bin/bash
#encoding=utf-8

import sys
import os
import re

target_string = 'debugMode'

#修改assets/sdkParams文件的debug模式，只需要输入
def move_apk_debug_mode(debug_mode, file_path):
	sdkparamter = file_path + '/assets/sdkParams.properties'
	print(sdkparamter)
	if not os.path.exists(sdkparamter) or not os.path.isfile(sdkparamter):
		print("the path is not exists or not a file")
		return
	sdk_params_file = open(sdkparamter, "r+", encoding='utf-8')
	lines = []
	pattern = re.compile(r'debugMode')							#正则表达式匹配
	for line in sdk_params_file:
		if pattern.match(line):									
			line = "debugMode = %s\n" % debug_mode				#匹配成功将修改debuge模式
		lines.append(line)
	sdk_params_file.close()
	sdk_params_file = open(sdkparamter,'w')
	sdk_params_file.writelines(lines)
	sdk_params_file.close()
	
if __name__ == '__main__':
	#参数一为你想要的模式，参数二为你的文件，文件目录为你的sdkParams.properties上面第二级目录
	print("参数一为你想要的模式，参数二为你的文件,形如：\n 脚本名 1 /C/sdkParams.properties")
	move_apk_debug_mode(sys.argv[1], sys.argv[2])
