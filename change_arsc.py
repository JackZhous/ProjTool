#!/bin/bash
#encoding=utf-8
#加密arsc文件，使apktool读取文件结构时无法读取

import os
import os.path
import struct
import sys

#修改resources.arsc文件，更改文件头大小，使apktool无法解析文件头
def sign_arsc_file(file):
	print(file)
	if not os.path.exists(file) or not os.path.isfile(file):
		print("the path is not exists or not a file")
		return
	arsc_file = open(file, "rb")
	data = arsc_file.read(12)										#读取文件头
	table_type_2,head2,file4,package4 = struct.unpack("2H2I", data)	#将二进制数据解包成具体的数据
	new_head2 = head2+8												#修改头大小
	head2 = 1
	file4 = file4 + 8												#修改整体文件大小
	new_data = struct.pack("2H2I4H", table_type_2, new_head2, file4, package4,head2,head2,head2,head2)												#在合成二进制数据
	new_file = open("a.arsc", 'wb')									#写入文件
	new_file.write(new_data)
	new_file.write(arsc_file.read())
	new_file.flush()
	new_file.close()
	arsc_file.close()
	

#sys.argv[1]是新的文件   sys.argv[2]是旧的文件
if __name__ == '__main__':
	sign_arsc_file(sys.argv[1])
