import csv 
import json 
import collections
from collections import OrderedDict

orderedDict = collections.OrderedDict()
numFiles = 49

def csv_to_json(csvFilePath, jsonFilePath, debug=0):
    index = OrderedDict([('index', {})])
    indexInner = {'_index' : 'usdafoods', '_id' : None}

    with open(csvFilePath, encoding='utf-8') as csvf: 
        with open(jsonFilePath, 'w', encoding='utf-8') as jsonf:
            csvReader = csv.DictReader(csvf) 
            for row in csvReader: 
                indexInner['_id'] = row['Food_Code']
                index['index'] = indexInner
                jsonString = json.dumps(index)

                if(debug):
                    print(jsonString)

                jsonf.write(jsonString)
                jsonf.write("\n")
                data = json.dumps(row)
                jsonf.write(data)
                jsonf.write("\n")
          
for i in range(1, numFiles):     
    print("On file {} ".format(i))     
    csvFilePath = "Nutrient_Values-{0}.csv".format(i)
    jsonFilePath = "Nutrient_Values-{0}.json".format(i)
    csv_to_json(csvFilePath, jsonFilePath)


