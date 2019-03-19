import pymysql
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException,StaleElementReferenceException
from selenium.webdriver.chrome.options import Options

import time
from datetime import datetime

import queue
# 连接数据库
def connectDb():
    try:
        db = pymysql.connect("localhost","username","password","dataBase", charset="utf-8")
        return db
    except Exception:
        print("the dataBase can not be connected")

# 设置浏览器驱动
def configChromeDriver():
	try:
		# chrome_options = Options()
		# chrome_options.add_argument('--headless')
		# chrome_options.add_argument('--disable-gpu')
		# path = 'D:\\WorkSoftWare\\chrome67\\chromedriver.exe'
		driver = webdriver.Chrome()
		return driver
	except Exception:
		print("Chrome driver is useless!")

# 阿里云服务器价格计算器
class Aliyun:
	def __init__(self, driver):
		
		self._driver = driver

	'''
	获取区域信息
	'''
	def get_region(self):
		# 地区选项卡     
		region_xpath = '/html/body/div[3]/div/div[2]/div[2]/div[2]/div/div/div[1]/form/dl[1]/dd/div[2]/div/span/span[2]'
						
		click1 = self._driver.find_element_by_xpath(region_xpath)
		click1.click()
		
		# 存储区域列表
		region_items = click1.find_elements_by_tag_name("li") 
		# region = []
		# for item in region_items:
		# 	region.append(item.text)

		# 模拟点击不同地区选项卡
		region_counter = 1 #地区列表计数器
		region_temp = region_xpath+'/ul/li'
		for item in region_items:
			print(item.text)
			self._driver.find_element_by_xpath(region_temp+'['+str(region_counter)+']').click()
			region_counter +=1
			click1.click()
			
			time.sleep(1)
			self.get_net()
			
	
	# 获取网络类型 
	def get_net(self):
		# 网络选项卡
		net_xpath = '/html/body/div[3]/div/div[2]/div[2]/div[2]/div/div/div[1]/form/dl[2]/dd/div[2]/div/span/span[2]'
					# /html/body/div[3]/div/div[2]/div[2]/div[2]/div/div/div[1]/form/dl[2]/dd/div[2]/div/span/span[2]/ul/li

		click2 = self._driver.find_element_by_xpath(net_xpath)
		click2.click()

		# 存储网络类型列表
		net_items = click2.find_elements_by_tag_name("li")
		# net = []
		# for item in net_items:
		# 	net.append(item.text)

		# 模拟点击不同网络类型
		net_counter = 1
		net_temp = net_xpath+'/ul/li'
		for item in net_items:
			print(item.text)
			self._driver.find_element_by_xpath(net_temp).click()
			time.sleep(1)
			self.get_instance()

	# 初始化进入规格详情页面
	def get_instance_init(self):
		# 实例规格
		instSpec_xpath = '/html/body/div[3]/div/div[2]/div[2]/div[2]/div/div/div[1]/form/dl[3]/dd/div[2]/div[2]/div/div/span[1]/span/span'
		click3 = self._driver.find_element_by_xpath(instSpec_xpath)
		click3.click()
	def get_instance(self):
		self.get_instance_init()
		# arch_all = queue.Queue() # 存储架构
		# kind_all = queue.Queue() # 存储计算类型
		instance_counter = 0 # 计数器
		instance_all = queue.Queue() #存储实例详细规格
		'''
		架构分类选项卡： x86计算 ,异构计算 GPU / FPGA
		'''
		spec_xpath = '/html/body/span[2]/div/div/div/div/div[2]/div/div/div[1]/div[1]/span[2]/span/span'
					  # /html/body/span[2]/div/div/div/div/div[2]/div/div/div[1]/div[1]/span[2]/span/span/span[1]/span
					  # /html/body/span[2]/div/div/div/div/div[2]/div/div/div[1]/div[1]/span[2]/span/span/span[2]/span
		ar_first = self._driver.find_element_by_xpath(spec_xpath)
		arch_items = ar_first.find_elements_by_class_name('button-light')
		# print(arch_items)
		# print(len(arch_items)) # 架构测试
		for item1 in arch_items:
			item1.click()
			# item1.send_keys(Keys.ENTER)
			# time.sleep(1)
			# arch_all.put(item1)
			instance_counter += 1
			# print(item.text)
			'''
			计算类型：通用型  计算型  内存型  大数据型  本地SSD  存储增强型  高主频型  入门级(共享)
			'''
			# 云服务器种类
			kind_xpath = '/html/body/span[2]/div/div/div/div/div[2]/div/div/div[1]/div[2]/span[2]/span/span'
			kind_first = self._driver.find_element_by_xpath(kind_xpath)
			kind_items = kind_first.find_elements_by_class_name('button-light')

			for item2 in kind_items:
				item2.click()
				# time.sleep(1)
				# kind_all.put(item2)
				instance_counter += 1
				# print(item.text)
				# 获取服务器配置详情
				try:
					select_xpath = '/html/body/span[2]/div/div/div/div/div[2]/div/div/div[2]/table/tbody'
					# /html/body/span[2]/div/div/div/div/div[2]/div/div/div[2]/table/tbody/tr[1]
					select_click = self._driver.find_element_by_xpath(select_xpath)
					select_items = select_click.find_elements_by_tag_name('tr')
					for i in select_items:
						items_spec = i.find_elements_by_tag_name('td')
						temp = ''
						for kk in range(1, len(items_spec)):
							if kk!=5:
								temp += (items_spec[kk].text+',')
						# print(temp)
						if temp == ",,":
							continue
						instance_all.put(temp)
						instance_counter += 1
					# time.sleep(10)
				except NoSuchElementException:
					print("暂无满足条件的实例规格，请切换到其他可用区或地域重试")
		self._driver.find_element_by_xpath('/html/body/span[2]/div/div/div/div/div[3]/span[2]').click() # 确定
		time.sleep(2)
				
		# while not instance_all.empty():
		# 	print(instance_all.get())
		# # # # # ################################################################
		# counter = arch_all.qsize() + kind_all.qsize() + instance_all.qsize()
		# if counter == instance_counter:
		# 	print("Yes")
		# else:
		# 	print("No")
		# print(instance_counter,counter)
		counter = instance_counter
		# print("共有选项数目:",counter)
		pointer = 1
		while pointer <= counter:
			self.get_instance_init()
			tt = instance_all.get()
			spec_xpath = '/html/body/span[2]/div/div/div/div/div[2]/div/div/div[1]/div[1]/span[2]/span/span'
					  # /html/body/span[2]/div/div/div/div/div[2]/div/div/div[1]/div[1]/span[2]/span/span/span[1]/span
					  # /html/body/span[2]/div/div/div/div/div[2]/div/div/div[1]/div[1]/span[2]/span/span/span[2]/span
			ar_first = self._driver.find_element_by_xpath(spec_xpath)
			arch_items = ar_first.find_elements_by_class_name('button-light')
			flag1 = False
			flag2 = False
			for item1 in arch_items:
				if flag1 == True:
					break
				time.sleep(1)
				item1.click()
				time.sleep(1)
				'''
				计算类型：通用型  计算型  内存型  大数据型  本地SSD  存储增强型  高主频型  入门级(共享)
				'''
				# 云服务器种类
				kind_xpath = '/html/body/span[2]/div/div/div/div/div[2]/div/div/div[1]/div[2]/span[2]/span/span'
				kind_first = self._driver.find_element_by_xpath(kind_xpath)
				kind_items = kind_first.find_elements_by_class_name('button-light')

				for item2 in kind_items:
					if flag2 == True:
						flag1 = True
						break
					item2.click()
					time.sleep(1)
					# 获取服务器配置详情
					try:
						select_xpath = '/html/body/span[2]/div/div/div/div/div[2]/div/div/div[2]/table/tbody'

						select_click = self._driver.find_element_by_xpath(select_xpath)
						select_items = select_click.find_elements_by_tag_name('tr')
						for item3 in select_items:
							temp = ''
							items_spec = item3.find_elements_by_tag_name('td')
							for kk in range(1, len(items_spec)):
								if kk!=5:
									temp += (items_spec[kk].text+',')
							if temp == ",,":
								continue
							# print(temp)
							if tt == temp:
								# print("bingo",pointer,tt)
								pointer += 1
								time.sleep(2)
								try:
									items_spec[0].find_element_by_tag_name('input').click() # 选中
								except NoSuchElementException:
									print("当前选项卡没有选中按钮")
								time.sleep(1)
								self._driver.find_element_by_xpath('/html/body/span[2]/div/div/div/div/div[3]/span[2]').click() # 确定
								time.sleep(2)
								flag2 = True;
								break
					except NoSuchElementException:
						print("暂无满足条件的实例规格，请切换到其他可用区或地域重试")
			print(tt)
			self.get_duration()
			
	# 付费方式以及时长
	def get_duration(self):

		pay_xpath = '/html/body/div[3]/div/div[2]/div[2]/div[2]/div/div/div[1]/form/dl[6]/dd/div[2]/div/div[1]/div/div[1]'
		duration_xpath = '/html/body/div[3]/div/div[2]/div[2]/div[2]/div/div/div[1]/form/dl[6]/dd/div[2]/div/div[2]/div/div[1]'
						  
		pay_ways = self._driver.find_element_by_xpath(pay_xpath).text.split('\n')
		duration = self._driver.find_element_by_xpath(duration_xpath).text.split('\n')
		# print(pay_ways)
		# print(duration)
		for i in range(len(pay_ways)):
		 	temp1 = pay_xpath
		 	self._driver.find_element_by_xpath(temp1+'/span['+str(i+1)+']/div/div').click()
		 	time.sleep(1) 
		 	for j in range(len(duration)):
		 		temp2 = duration_xpath
		 		self._driver.find_element_by_xpath(temp2+'/span['+str(j+1)+']/div/div').click()
		 		time.sleep(1)
		 		print(pay_ways[i],duration[j])
		 		self._driver.find_element_by_xpath('/html/body/div[3]/div/div[2]/div[2]/div[2]/div/div/div[2]/span/div').click()
		 		time.sleep(5)
		 		a,b,c = self.get_price()
		 		print(a,'\n', b,'\n', c)
	
	# 获取云产品价格
	def get_price(self):
		self._driver.find_element_by_xpath('/html/body/div[3]/div/div[2]/div[2]/div[2]/div/div/div[2]/span/div').click()
		time.sleep(3)
		region  = self._driver.find_element_by_xpath('//*[@id="export-analysis-result"]/div[2]/h2/small').text
		thead = self._driver.find_elements_by_xpath('//*[@id="export-analysis-result"]/div[2]/table/thead')[0].text
		region_list = region.split('：')[-1]
		thead_list = thead.split(' ')
		clickF = self._driver.find_elements_by_xpath('//*[@id="export-analysis-result"]/div[2]/table/tbody')[0]

		contents = clickF.find_element_by_tag_name('tr').find_elements_by_tag_name('td')
		instance = list()
		for item in contents:
			instance.append(item.text)
		# print(region_list)
		# print(thead_list)
		# print(instance)
		return region, thead, instance
	
	# 开始
	def ecsInstancePrice(self):

		url = "https://tco.aliyun.com/tco/ecs/calculator"
		self._driver.get(url)
		time.sleep(1)
		self.get_region()
		# return self.get_price()

class DbOperate:
	def __init__(self, db, driver):
		self._db = db
		self._cursor = self._db.cursor()
		self._driver = driver

	def insert(self):
		ali = Aliyun(self._driver)
		ali.ecsInstancePrice()
		# print(region, thead, instance)



if __name__ == '__main__':
	db = connectDb()
	driver = configChromeDriver()
	DbOperate(db, driver).insert()
	