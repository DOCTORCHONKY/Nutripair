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
		if not pd.isnull(row["MENU ITEM"]): #if cell is not null
			food_data[row["MENU ITEM"]] = defaultdict(str)
			currMenuItem = row["MENU ITEM"]
		else:
			if (row["RAW"] == 'x'):				
				food_data[currMenuItem][row["INGREDIENTS"]] = (row["MEASUREMENTS"],1)
			else:
				food_data[currMenuItem][row["INGREDIENTS"]] = (row["MEASUREMENTS"],0)

	
	return food_data
		


