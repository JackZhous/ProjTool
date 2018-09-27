#!/bash/bin
#encoding=utf-8
from charger import EasyCharger
from scipy.misc import imread
from alarmMonitor import AMonitor
from wordcloud import WordCloud,ImageColorGenerator
import tkFileDialog
from Tkinter import *
from tkinter import messagebox
import matplotlib.pyplot as plt
import tkFont
import os
import sys

class MnitorAlarm:
	def __init__(self, charger, alarm):
		self.alarmfile = '告警.xlsx'
		self.server = 'ChongQing2'
		self.charger = charger			#充电管理类
		self.alarm = alarm
		self.chargerManager = None
		self.window = Tk()		#创建一个窗口
		self.window.geometry('800x600+0+0')		#大小
		self.window.title('和易充项目异常数据分析工具')
		self.code = StringVar()				#验证码
		self.stationName = StringVar()			#查询电站名称
		self.date = StringVar()
		self.label_font = tkFont.Font(family='Helvetica', size=15)
		self.input_font = tkFont.Font(family='Helvetica', size=12)
		self.author_font = tkFont.Font(family='Fixdsys', size=20)
		self.init_ui_menu()
		self.init_ui()
		self.window.mainloop()
		

	def init_ui_menu(self):
		self.menuBg = Menu(self.window)
		ServerMenu = Menu(self.menuBg)
		ServerMenu.add_command(label="ChongQing2", command=self.chongqing2)  
		ServerMenu.add_command(label="HeChi", command=self.hechi)
		self.menuBg.add_cascade(label="服务器环境选择", menu=ServerMenu)
		self.window.config(menu=self.menuBg)
	
	def chongqing2(self):
		if 'ChongQing2' == self.server:
			return
		self.server = 'ChongQing2'
		self.chooseServer()

	def hechi(self):
		if 'hechi' == self.server:
			return
		self.server = 'hechi'
		self.chooseServer()

	def chooseServer(self):
		if 'hechi' == self.server:
			self.server_str['text'] = '河池服务器'
			self.charger.update_net(2)
		else:
			self.server_str['text'] = '重庆第二套环境'
			self.charger.update_net()
		self.freshImage()

	def initCharger(self):
		mCode = self.code.get()
		print mCode
		ret = self.charger.login(mCode)
		if ret != 'true':
			messagebox.showinfo(title='告警提示', message = '初始化失败，请刷新验证码重新初始化')
			return
		filename = 'station所有站点名称汇总.txt'
		if os.path.exists(filename):
			return
		self.alarm.saveAllStationNameToFile(filename)

	def init_ui(self):
		self.server_str = Label(self.window, text='重庆第二套环境', font=self.label_font, fg='red')
		self.server_str.pack(side=TOP)
		Button(self.window, text='点我刷新验证码',command=self.freshImage).pack(pady = 5)
		ret = self.charger.validation()
		photo = PhotoImage(file = 't.gif')
		self.imgLabel = Label(self.window, image = photo)
		self.imgLabel.image = photo
		self.imgLabel.pack()
		Label(self.window, text='输入验证码', font=self.label_font).pack(pady=5)
		Entry(self.window, borderwidth = 3, width = 30, textvariable=self.code, font=self.input_font).pack(side=TOP)
		Button(self.window, text='必须点击初始化',command=self.initCharger).pack(pady = 5)
		Label(self.window,  text='输入电站名称或者端口号', font=self.label_font).pack(side=TOP)
		Entry(self.window, borderwidth = 3, width = 30, textvariable=self.stationName, font=self.input_font).pack(side=TOP)
		Label(self.window,  text='告警日期过滤,如208-3-2~208-4-3', font=self.label_font).pack(side=TOP)
		Entry(self.window, borderwidth = 3, width = 30,textvariable=self.date, font=self.input_font).pack(side=TOP)
		Button(self.window, text='开始查询',command=self.startMontior).pack(pady = 5)
		Button(self.window, text='大数据所有站点告警分析',command=self.startMontiorBigData).pack(pady = 5)
		tips = '工具使用说明：\n 1. 填入验证码必须点击初始化 \n 2. 输入指定电站名字捕获该电站下的所有告警\n 3.某一个时间段内该电站的告警，注意格式\n 4. 点击\'开始分析\'按钮开始分析 \n 特别说明：如果第一项不输入，第二项生成的文件默认在当前路径；\n如果第一项有输入，第二项生成的文件默认保存在第一项文件存放处'
		Label(self.window, text='author: JackZhous -- ^_^', font=self.author_font).pack(side=BOTTOM, pady=0)
		Label(self.window, text='感谢你的使用 --- 和易充异常数据统计工具', font=self.author_font).pack(side=BOTTOM, pady=0)
		Label(self.window, text=tips, font=self.label_font, fg='blue').pack(side=BOTTOM, pady=0)
	

	# 刷新图片事件
        def freshImage(self):
                ret = self.charger.validation()
                photo = PhotoImage(file = 't.gif')
                self.imgLabel.config(image=photo)
                self.imgLabel.image = photo

	def startMontior(self):
		name_or_port = self.stationName.get()
		time = self.date.get()
		ret = 0
		new_file = os.getcwd() + os.path.sep +  name_or_port + self.alarmfile
		if name_or_port.isdigit():
			ret = self.alarm.searchAlarmWithPort(name_or_port, time)
		else:
			ret = self.alarm.searchAlarmWithStation(name_or_port, time)
		if ret == 0:
			messagebox.showinfo(title='告警提示', message = '无告警')
		elif ret == 1:
			self.alarm.saveFile(name_or_port + self.alarmfile)
			messagebox.showinfo(title='告警提示', message = '告警日志查询成功，保存文件在' + new_file)
		else:
			messagebox.showinfo(title='告警提示', message = '网络异常')

	#大数据分析
	def startMontiorBigData(self):
		ret = self.alarm.searchAllStation(self.date.get())
		if ret == 'false':
			return
		alarmEventFile = open('even.txt', 'w')
		alarmAddrFile  = open('addr.txt', 'w')
		for item in ret:
			try:
				alarmEventFile.write(item['alarmEvent'] + ' ')
				alarmEventFile.write(item['alarmRemark'] + ' ')
				alarmAddrFile.write(item['deviceStation'] + ' ')
			except:
				alarmAddrFile.write(item['handlePerson'] + ' ')
				print item
		alarmEventFile.close()
		alarmAddrFile.close()
		self.wordsColud()	
	
	def wordsColud(self):
		backgroud_Image = imread(sys.path[0] + os.path.sep + '1.png')
		text = open(os.path.join('even1.txt')).read().decode('utf-8')
		font = os.path.join(os.path.dirname(__file__), "DroidSansFallbackFull.ttf")
		#wordcloud = WordCloud(font_path=font,mask = backgroud_Image, max_words = 500, max_font_size = 50, random_state = 30).generate(text)
		wordcloud = WordCloud(font_path=font,max_font_size=300, mask = backgroud_Image, max_words = 100).generate(text)
#		image_colors = ImageColorGenerator(backgroud_Image)
#		wordcloud.recolor(color_func = image_colors)
		plt.imshow(wordcloud)
		plt.axis("off")
		plt.show()

if __name__ == '__main__':
	reload(sys)
	sys.setdefaultencoding('utf-8')
	charger = EasyCharger('alarm')
	alarm = AMonitor(charger)
	MnitorAlarm(charger, alarm)
