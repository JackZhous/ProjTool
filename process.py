#!/bin/bash
#coding=utf-8


import re
import subprocess
import os
import platform

class MyProcess:
	base_dir = os.path.dirname(__file__)	#cuurent absoulte path	
	def __init__(self, task_name):
		self.task_name = task_name

	#执行外部程序
	def exec_cmd(self, cmd):
		cmd = cmd.replace('\\', '/')
		cmd = re.sub('/+', '/', cmd)
		
		if platform.system() == 'Windows':
			child_process = subprocess.STARTUPINFO
			child_process.dwFlags = subprocess.STARTF_USESHOWWINDOW
			child_process.wShowWindow = subprocess.SW_HIDE
			cmd = cmd.encode('gbk')
		
		result = subprocess.Popen(cmd, shell=True)
		print('start exec cmd: ' + cmd)
		ret = result.wait()
		result = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)			#通过管道拿取输出在cmd上的内容
		std_output, err_output = result.communicate()
		if ret:
			print('exec  cmd failed' +  err_output)
		else:
		#	if 'success' in std_output:
		#		print('exec ' + cmd + ' --- success')
			return True
		return False
	
	# 签名文件 apk  签名密码 签名别名
	def exec_sign_apk(self, apk_path):
		keypass = 'wsdyi100'
		keyales = 'jackzhous'
		#sign_file = '/Users/sever1/shell/third/boxing.keystore'
		sign_file = self.base_dir + "/boxing.keystore"
		cmd = 'jarsigner -digestalg SHA1 -sigalg MD5withRSA -keystore %s -storepass %s -keypass %s %s %s' % (sign_file, keypass, keypass, apk_path, keyales)
		result = self.exec_cmd(cmd)
		return result 
		
	#apk解包
	def apktool_d(self, apk_file, output_file):
		apktool_jar = self.base_dir + '/apktool.jar'
		cmd = 'java -jar %s -d %s -fo %s' % (apktool_jar, apk_file, output_file)
		result = self.exec_cmd(cmd)
		return result
	
	#apk合包
	def apktool_b(self, output_file):
		apktool_jar = self.base_dir + '/apktool.jar'
		cmd = 'java -jar %s b %s' % (apktool_jar, output_file)
		result = self.exec_cmd(cmd)
		return result
		
if __name__ == '__main__':
	process_main()
