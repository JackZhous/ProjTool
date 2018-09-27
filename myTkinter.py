#!/bash/bin
#encoding=utf-8
from charger import EasyCharger
from testCharger import ChargerManager
import tkFileDialog
from Tkinter import *
from tkinter import messagebox
import tkFont
import os
import sys

class ChargeDataAnalysis:
	def __init__(self, charger):
		self.server = 'ChongQing2'
		self.charger = charger			#充电管理类
		self.chargerManager = None
		self.window = Tk()		#创建一个窗口
		self.window.geometry('800x600+10+10')		#大小
		self.window.title('和易充项目异常数据分析工具')
		self.old_file_path = StringVar()		#历史文件
		self.new_file = StringVar()			#新文件
		self.code = StringVar()				#验证码
		self.datetime = StringVar()			#用于过滤订单的起止时间
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
			self.charger.update_net(1)
		self.freshImage()

	def init_ui(self):
		self.server_str = Label(self.window, text='重庆第二套环境', font=self.label_font, fg='red')
		self.server_str.pack(side=TOP)
		la = Label(self.window,  text='输入昨日统计文件', font=self.label_font)
		la.pack(side=TOP)
		history_file = Entry(self.window, state = 'disabled',borderwidth = 3, width = 30, textvariable=self.old_file_path, font=self.input_font)
		history_file.pack(side=TOP)
		history_file.bind('<ButtonPress>',self.click_input)
		datetime = Label(self.window,  text='输入起止时间', font=self.label_font)
		datetime.pack(side=TOP)
		datetimeS = Entry(self.window, borderwidth = 3, width = 30,textvariable=self.datetime, font=self.input_font)
		datetimeS.pack(side=TOP) 
		newfilelabel = Label(self.window,  text='输入今日统计文件名', font=self.label_font)
		newfilelabel.pack(side=TOP)
		newfile = Entry(self.window, borderwidth = 3, width = 30,textvariable=self.new_file, font=self.input_font)
		newfile.pack(side=TOP)
		Label(self.window, text='输入验证码', font=self.label_font).pack(pady=5)
		Button(self.window, text='点我刷新验证码',command=self.freshImage).pack(pady = 5)
		ret = self.charger.validation()
		photo = PhotoImage(file = 't.gif')
		self.imgLabel = Label(self.window, image = photo)
		self.imgLabel.image = photo
		self.imgLabel.pack()
		tips = '工具使用说明：\n 1. 输入昨日该工具创建的文件（第一次使用可以不填）\n 2. 输入今日保存数据的文件名\n 3. 输入验证码（如果验证码长时间没输入，需要刷新验证码在进行输入）\n 4. 点击\'开始分析\'按钮开始分析 \n 特别说明：如果第一项不输入，第二项生成的文件默认在当前路径；\n如果第一项有输入，第二项生成的文件默认保存在第一项文件存放处'
		Entry(self.window, borderwidth = 3, width=30, textvariable=self.code, font= self.input_font).pack()
		Button(self.window, text="开始分析", command=self.click_start_aya).pack()
		Label(self.window, text='author: JackZhous -- ^_^', font=self.author_font).pack(side=BOTTOM, pady=10)
		Label(self.window, text='感谢你的使用 --- 和易充异常数据统计工具', font=self.author_font).pack(side=BOTTOM, pady=10)
		Label(self.window, text=tips, font=self.label_font, fg='blue').pack(side=BOTTOM, pady=10)
	# 输入的历史文件		
	def click_input(self,event):
		filename = tkFileDialog.askopenfilename(initialdir = os.getcwd())
		self.old_file_path.set(filename)
	
	# 分析开始点击事件
	def click_start_aya(self):
		old_file = self.old_file_path.get()
		new_file = self.new_file.get()
		code = self.code.get()
		time = self.datetime.get()
		# 判断输入是否完全
		if code == '' or new_file == '':
			messagebox.showinfo(title='分析数据失败', message = '请输入创建的文件名和验证码')
			return 'false'
		# 自动添加文件后缀
		if not new_file.endswith('.xlsx'):
			new_file = new_file + '.xlsx'
		# 保存位置
		if old_file != '':
			paths = old_file.split(os.path.sep)
			new_file_path = ''
			for index in range(len(paths) - 1):
				new_file_path = new_file_path + paths[index] + os.path.sep
			new_file = new_file_path + new_file
		else:
			new_file = os.getcwd() + os.path.sep +  new_file 
		if self.chargerManager is None:
			self.chargerManager = ChargerManager(self.charger)
		ret = self.chargerManager.main(old_file, new_file, code, time)
		if ret != 'true':
			messagebox.showinfo(title='结果提示', message = '失败\n'+ ret)
		else: 
			messagebox.showinfo(title = '结果提示', message = ('成功\n文件存放在:%s'%new_file))
	
	# 刷新图片事件
	def freshImage(self):
		ret = self.charger.validation()
		photo = PhotoImage(file = 't.gif')
		self.imgLabel.config(image=photo)
		self.imgLabel.image = photo

	

if __name__ == '__main__':
	charger = EasyCharger('xxx')
	dataA = ChargeDataAnalysis(charger)
