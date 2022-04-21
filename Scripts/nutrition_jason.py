'''
nutrition_jason.py

APIs to read, organize, query, and calculate nutrition labels given restaurant excel data (ingredients and measurements)

by: Jason Nguyen
'''

import pandas as pd
from collections import defaultdict
from opensearchpy import OpenSearch, RequestsHttpConnection, AWSV4SignerAuth
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
	nutrition_info = {}

	index_name = 'usdafoods'
	client = connect()
	q = ingredient
	query = {
	'size': 5,
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

	for i in range(response["hits"]["total"]["value"] if response["hits"]["total"]["value"] <= 10 else 10):
		try:
			print("Food: ", i, "Protein_g: ", response["hits"]["hits"][i]["_source"]["Protein_g"], "Category: ", response["hits"]["hits"][i]["_source"]["Food_Description"])
		except:
			break


''' 
calculate_nutrition()
Input: (dict: food_data)
Output: (dict: nutrition_labels)
'''
def calculate_nutrition(food_data):
	pass




if __name__ == "__main__":

	print("Calculating Nutrition Labels for Jan's Health Bar")

	# Restaurant Food Item Data
	fileName = "Jan's Health Bar (SAMPLE MENU).xlsx"
	# Read food item data
	food_data = read_excel(fileName)
	# Query milk
	query_ingredient("milk")

