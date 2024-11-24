import pandas as pd
from PyQt6.QtWidgets import QDialog, QMessageBox

import View
from variable import *


class MainWindow(QDialog):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.setWindowTitle('御魂计算器')
		self.ui = View.Ui_Dialog()
		self.ui.setupUi(self)
		self.data_df = self.load_data_from_xlsx(execl_file_path)
	def populate_comboboxes(self, df):
		"""填充下拉框"""
		name = df['御魂'].drop_duplicates()
		match_data = df['主属性'].drop_duplicates()
		for i in name:
			self.ui.name_choice.addItem(str(i))
		for i in match_data:
			self.ui.Primary_attribute_box.addItem(str(i))
	
	def load_data_from_xlsx(self, file_path):
		"""加载下拉框"""
		try:
			# 读取 Excel 文件
			df = pd.read_excel(file_path)
			self.populate_comboboxes(df)
			return df
		except FileNotFoundError:
			print(f"File {file_path} not found.")
			return None
		except pd.errors.ParserError:
			print(f"Error parsing the file {file_path}.")
			return None
		except Exception as e:
			print(f"An unexpected error occurred: {e}")
			return None
	
	def display_data(self):
		data = {
			"御魂": self.ui.name_choice.currentText(),
			"位置": self.ui.Stand_line.currentText(),
			"主属性": self.ui.Primary_attribute_box.currentText(),
			"攻击加成": self.ui.Attack_line.text(),
			"暴击": self.ui.BaoJi_line.text(),
			"爆伤": self.ui.BaoShang_line.text(),
			"速度": self.ui.Speed_line.text(),
			"效果命中": self.ui.Effect_hits_line.text(),
			"效果抵抗": self.ui.Effect_Resistant_line.text(),
			"防御加成": self.ui.FangYu_line.text(),
			"生命加成": self.ui.ShengMing_line.text()
		}
		return data
	
	def convert_value(self, attr, value, conversion_factors):
		"""Count的辅助"""
		if attr in conversion_factors and value:
			return round(float(value) / conversion_factors[attr], 3)
		return value
	
	def Count(self):
		"""计算几手，简单收益"""
		data = self.display_data()
		conversion_factors = {
			"暴击": 2.7,
			"速度": 2.7,
			"攻击加成": 2.7,
			"防御加成": 2.7,
			"生命加成": 2.7,
			"效果命中": 3.6,
			"效果抵抗": 3.6,
			"爆伤": 3.6
		}
		try:
			revenue = {attr: self.convert_value(attr, value, conversion_factors) for attr, value in data.items()}
			return revenue
		except Exception as e:
			print(f"An error occurred: {e}")
			return {}
	def Revenue_Count(self):
		"""计算御魂对应execl的位置"""
		count1 = self.Count()
		if self.data_df is None:
			return None
		if count1['位置'] == "1号位" or count1['位置'] == "3号位" or count1['位置'] == "5号位":
			count1['位置'] = "1、3、5号位"
			df_filter = self.data_df[
				(self.data_df['御魂'] == count1['御魂']) & (self.data_df['位置'] == count1['位置'])]
			return df_filter
		else:
			try:
				print("各类收益", count1)
				df_filter = self.data_df[
					(self.data_df['御魂'] == count1['御魂']) & (self.data_df['位置'] == count1['位置']) & (
							self.data_df['主属性'] == count1['主属性'])]
				return df_filter
			except Exception as e:
				print(f"An error occurred: {e}")
	
	def final_count(self):
		"""计算最终收益"""
		revenue = self.Count()
		for x in revenue:
			if revenue[x] == "":
				revenue[x] = "0"
		print("御魂属性为 ", revenue)
		revenue_filter = self.Revenue_Count()
		final_count = 0
		EXCLUDED_KEYS = ["御魂", "位置", "主属性"]
		for x in revenue:
			values = revenue_filter[x].values if x in revenue_filter else None
			if x in EXCLUDED_KEYS:
				continue
			elif values == "极限":
				if float(revenue[x]) > 4:
					final_count = round(float(revenue[x]), 3)
					QMessageBox.information(self, "御魂计算结果",
											f"极限收益！有效御魂为: {x}，最终收益为：{final_count} 手")
					return final_count
			elif values == 1:
				final_count += round(float(revenue[x]), 3)
			else:
				final_count += 0
		print("最终有效收益为 ", round(final_count, 3))
		result = {
			key: round(float(revenue[key]), 3)
			for key in revenue
			if
			key in revenue_filter and revenue_filter[key] is not None and key not in EXCLUDED_KEYS and isinstance(
				revenue[key], (int, float))
		}
		QMessageBox.information(self, "御魂计算结果", "御魂属性为：" + str(revenue)
								+ "\n有效属性为：" + str(result)
								+ f"\n御魂最终收益为：{str(round(final_count, 3))} 手")
		return final_count
	
	def button_Count1_click(self):
		self.final_count()
		
	def name_choice_changed(self):
		self.ui.Primary_attribute_box.clear()
		df = pd.read_excel('../resource/御魂属性.xlsx')
		y=self.ui.Stand_line.currentText()
		if y == "1号位" or y == "3号位" or y == "5号位":
			y = "1、3、5号位"
		print(y)
		df1=df[(df['御魂'] == self.ui.name_choice.currentText())&(df['位置']==y)].drop_duplicates()
		print(df1)
		for i in df1['主属性'].drop_duplicates():
			self.ui.Primary_attribute_box.addItem(str(i))