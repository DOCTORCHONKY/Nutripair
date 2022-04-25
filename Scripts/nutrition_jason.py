'''
nutrition_jason.py

APIs to read, organize, query, and calculate nutrition labels given restaurant excel data (ingredients and measurements)

by: Jason Nguyen
'''

import pandas as pd
from collections import defaultdict
from opensearchpy import OpenSearch, RequestsHttpConnection
import boto3

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
			food_data[row["MENU ITEM"]] = defaultdict(tuple)
			currMenuItem = row["MENU ITEM"]
		# if menu item cell is null, we are working with previous menu item
		else:
			# food_data[currentMenuItem][ingredient] = (measurement,raw/not raw)
			# RAW = 1, NOT RAW = 0
			if (row["RAW"] == 'x'):				
				food_data[currMenuItem][row["INGREDIENTS"]] = (float(row["MEASUREMENTS"]),1)
			else:
				food_data[currMenuItem][row["INGREDIENTS"]] = (float(row["MEASUREMENTS"]),0)

	# return dictionary with all food ingredient data
	return food_data


'''
connect()
Input: None
Output: None
'''
def connect():
	host = 'https://search-nutripair-dev2-toqicucpwv65awgbezwshuwbvy.us-west-1.es.amazonaws.com' # cluster endpoint, for example: my-test-domain.us-east-1.es.amazonaws.com
	region = 'us-west-1' # e.g. us-west-1
	awsauth = ("capstone", "Nutripairrocks123!")


	client = OpenSearch(
		hosts = host,
		port = 403,
		http_auth = awsauth,
		use_ssl = True,
		verify_certs = True,
		connection_class = RequestsHttpConnection
	)

	return client

'''
query_food()
Input: (string: foodItem)
Output: (dict[nutrition]: nutritionInformation)
'''
def query_ingredient(ingredient):
	nutrition_info = defaultdict(float)

	index_name = 'usdafoods'
	client = connect()
	q = ingredient
	query = {
	'size': 10,
	'query': {
		'multi_match': {
		'query': q
		}
	}
	}

	response = client.search(
		body = query,
		index = index_name
	)

	print('\nSearch results:')
	print(response)
	
	
	try:
		print("Food: ", 0, "Category: ", response["hits"]["hits"][0]["_source"]["Food_Description"])
		nutrition_info["CALORIES"] = float(response["hits"]["hits"][0]["_source"]["Energy_kcal"])
		print("CALORIES: ", response["hits"]["hits"][0]["_source"]["Energy_kcal"])
		nutrition_info["TOTAL FAT (g)"] =  float(response["hits"]["hits"][0]["_source"]["Total_Fat_g"])
		print("TOTAL FAT (g): ", response["hits"]["hits"][0]["_source"]["Total_Fat_g"])
		nutrition_info["SATURATED FAT (g)"] = float(response["hits"]["hits"][0]["_source"]["Saturated_Fat_g"])
		print("SATURATED FAT (g): ", response["hits"]["hits"][0]["_source"]["Saturated_Fat_g"])
		nutrition_info["TRANS FAT (g)"] = float(response["hits"]["hits"][0]["_source"]["Monounsaturated_Fat_g"]) # MISSING
		print("TRANS FAT (g): ", response["hits"]["hits"][0]["_source"]["Monounsaturated_Fat_g"])
		nutrition_info["CHLOESTEROL (mg)"] = float(response["hits"]["hits"][0]["_source"]["Cholesterol_mg"])
		print("CHLOESTEROL (mg): ", response["hits"]["hits"][0]["_source"]["Cholesterol_mg"])
		nutrition_info["SODIUM (mg)"] = float(response["hits"]["hits"][0]["_source"]["Sodium_mg"])
		print("SODIUM (mg): ", response["hits"]["hits"][0]["_source"]["Sodium_mg"])
		nutrition_info["TOTAL CARBOHYDRATE (g)"] = float(response["hits"]["hits"][0]["_source"]["Carbohydrate_g"])
		print("TOTAL CARBOHYDRATE (g): ", response["hits"]["hits"][0]["_source"]["Carbohydrate_g"])
		nutrition_info["DIETARY FIBER (g)"] = float(response["hits"]["hits"][0]["_source"]["Total_Dietary_Fiber_g"])
		print("DIETARY FIBER (g): ", response["hits"]["hits"][0]["_source"]["Total_Dietary_Fiber_g"])
		nutrition_info["TOTAL SUGARS (g)"] = float(response["hits"]["hits"][0]["_source"]["Total_Sugars_g"])
		print("TOTAL SUGARS (g): ", response["hits"]["hits"][0]["_source"]["Total_Sugars_g"])
		nutrition_info["ADDED SUGARS (g)"] = 0
		print("ADDED SUGARS (g): ", "0") # MISSING
		nutrition_info["PROTEIN (g)"] = float(response["hits"]["hits"][0]["_source"]["Protein_g"])
		print("PROTEIN (g): ", response["hits"]["hits"][0]["_source"]["Protein_g"])
		nutrition_info["VITAMIN D (mcg)"] = float(response["hits"]["hits"][0]["_source"]["Vitamin_D_mcg"]) # MCG not MG
		print("VITAMIN D (mcg): ", response["hits"]["hits"][0]["_source"]["Vitamin_D_mcg"]) 
		nutrition_info["CALCIUM (mg)"] = float(response["hits"]["hits"][0]["_source"]["Calcium_mg"])
		print("CALCIUM (mg): ", response["hits"]["hits"][0]["_source"]["Calcium_mg"])
		nutrition_info["IRON (mg)"] = float(response["hits"]["hits"][0]["_source"]["Iron_mg"])
		print("IRON (mg): ", response["hits"]["hits"][0]["_source"]["Iron_mg"])
		nutrition_info["POTASSIUM (mg)"] = float(response["hits"]["hits"][0]["_source"]["Potassium_mg"])
		print("POTASSIUM (mg): ", response["hits"]["hits"][0]["_source"]["Potassium_mg"])
	except:
		print("Can't find ingredient")
	

	return nutrition_info

''' 
calculate_nutrition()
Input: (dict: food_data)
Output: (dict: nutrition_labels)
'''
def calculate_nutrition(food_data):
	nutrition_labels = {}
	for food, ingredients in food_data.items():
		print("Food Item: ", food)
		for ingredient, details in ingredients.items():
			print("Ingredient: ", ingredient)
			measurement = details[0]
			print("Measurement: ", measurement)
			raw = details[1]
			print("Raw: ", raw)


			'''
			if (raw):
				nutrition_info = query_ingredient("RAW" + ingredient)
			else:
				nutrition_info = query_ingredient(ingredient)
			'''

			nutrition_info = query_ingredient(ingredient)
			
			nutrition_labels[food] = defaultdict(float)

			for label, value in nutrition_info.items():
				nutrition_labels[food][label] += float(value) * measurement
				#nutrition_labels[food][label] += value * 2
		
	
	print(nutrition_labels)
	return nutrition_labels
			




if __name__ == "__main__":

	print("Calculating Nutrition Labels for Jan's Health Bar")

	# Restaurant Food Item Data
	fileName = "Jan's Health Bar (SAMPLE MENU).xlsx"
	# Read food item data
	food_data = read_excel(fileName)
	# Calculate nutrition labels for food_data
	nutrition_labels = calculate_nutrition(food_data)

