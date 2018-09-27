#!/bin/bash
#比较两个androidmainfest.xml的不同   

import os
import os.path
import xml.etree.ElementTree as ET
import sys
import time

android="http://schemas.android.com/apk/res/android"
file_name = ""
__author__ = "Jackzhous"

#比较的主函数
def compare(source , des):
    if not os.path.exists(des):
        print( des,'is not exist')
        return
    if not os.path.exists(source):
        print(source, 'is not exist')
        return
    ET.register_namespace('android',android)
    source_tree = ET.parse(source)
    des_tree = ET.parse(des)
    find_different(source_tree, des_tree, "uses-permission")
    find_different(source_tree, des_tree, "application/activity")
    find_different(source_tree, des_tree, "application/receiver")
    find_different(source_tree, des_tree, "application/service")
    find_different(source_tree, des_tree, "application/meta-data")


msg = "we need add:\n"

#根据类别查找两个文件是否相同
def find_different(s_tree, d_tree, key):
    msg = "we need add: \n " + key + "  "
    flag = 0
    for target in s_tree.findall(key):
        name = target.get("{%s}name"%android)
        target = check_node_is_exist(d_tree,name, key)
        if target == 2:
            msg += name + '\n'
            flag = 1
    if flag == 1:
        save_msg_to_file(msg)

#检查目标文件是否存在这个节点
def check_node_is_exist(tree, name, key):
    target = tree.find(key + "[@{" + android + "}name='" + name + "']")
    if target is None:
        print("we need " ,key, " ---", name)
        return 2
    else:
        return 1

#获取当前时间
def get_now_time():
    return time.strftime("%Y-%m-%d-%H-%M-%S.txt", time.localtime(time.time()))

#保存内容到文件
def save_msg_to_file(msg):
    fp = open(file_name,'a')
    fp.write(msg)
    fp.write('\n')
    fp.flush()
    fp.close()

#sys.argv[1]是新的文件   sys.argv[2]是旧的文件
if __name__ == '__main__':
	print("* ----title----- compare android manifest xml ------------------ *")
	print("* ----author----         ", __author__ , "          ------------------ *")
	print("* ----note------ writen on 2016-04-18, this   ------------------ *")
	print("* -------------- program is used to compare   ------------------ *")
	print("* -------------- two dierent xml ,and get the ------------------ *")
	print("* -------------- difference                   ------------------ *")
	file_name = os.getcwd() + os.sep + get_now_time()
	compare(sys.argv[1], sys.argv[2])
	print("*the difference file is located: *",file_name)