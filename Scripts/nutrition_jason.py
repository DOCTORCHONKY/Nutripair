'''
nutrition_jason.py

APIs to read, organize, query, and calculate nutrition labels given restaurant excel data (ingredients and measurements)

by: Jason Nguyen
'''

import pandas as pd
from collections import defaultdict

'''
read_excel()
Input: (string: fileName)
Output: (dict: food_data)
'''
def read_excel(fileName):
	#need to change parameters if reading a different excel sheet, and/or depending on where the column headers are
	excel_data = pd.read_excel("Jan's Health Bar (SAMPLE MENU).xlsx", header=5)

	# food_data
	# {string menu item: {string ingredient: (float measurements, boolean raw)}}
	food_data = defaultdict(str)

	# current menu item
	currMenuItem = ""

	# iterate through excel sheet
	for i, row in excel_data.iterrows():
		# if menu item cell is not null -> add it as a menu item
		if not pd.isnull(row["MENU ITEM"]):
			food_data[row["MENU ITEM"]] = defaultdict(str)
			currMenuItem = row["MENU ITEM"]
		# if menu item cell is null, we are working with previous menu item
		else:
			# food_data[currentMenuItem][ingredient] = (measurement,raw/not raw)
			# RAW = 1, NOT RAW = 0
			if (row["RAW"] == 'x'):				
				food_data[currMenuItem][row["INGREDIENTS"]] = (row["MEASUREMENTS"],1)
			else:
				food_data[currMenuItem][row["INGREDIENTS"]] = (row["MEASUREMENTS"],0)

	# return dictionary with all food ingredient data
	return food_data

'''
calculate_nutrition()
Input: (dict: food_data)
Output: (dict: nutrition_labels)
'''
def calculate_nutrition(food_data):
	pass
		


