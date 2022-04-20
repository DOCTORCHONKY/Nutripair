import pandas as pd


#need to change parameters if reading a different excel sheet, and/or depending on where the column headers are
excel_data = pd.read_excel("Jan's Health Bar (SAMPLE MENU).xlsx", header=5)

#1st param list for when we write to excel
data_list = []

#to use for checking if it is the first menu item
empty_list = [0 for x in range(10)]
#to use as the lists inside data_list
temp_l = [0 for x in range(10)]

#iterate through excel sheet
for i, row in excel_data.iterrows():
    if not pd.isnull(row["MENU ITEM"]):#if cell is not null
        if temp_l == empty_list:#don't add to data list yet, this is the first menu item, continue iterating through rows
            pass#copy what is inside the elif into here, or set a flag and replace elif with if statement checking flag
        data_list.append(temp_l)
        temp_l = [0 for x in range(10)]#reset temp_l in case there is more dishes
        #print(row["MENU ITEM"])
    elif pd.isnull(row["MENU ITEM"]):#if cell is null, maybe replace with else instead of elif
        #print("OMG")
        pass#filler, can remove later
        #
        #calculate nutrition values
        #change temp_l indices as needed by doing temp_l[i] += [insert calculated nutrition value here]
        

#TEST IF CAN INDEX row BY HEADER NAME, WORKS!!!
#to make dataframe: df = pd.DataFrame([[11, 21, 31], [12, 22, 32], [31, 32, 33]],index=['one', 'two', 'three'], columns=['a', 'b', 'c'])
#1st parameter = list of lists of nutrition info in order of column headers. 1st parameter list in order of dishes read in from excel
    # can create 1st parameter list at start of code and then each list when we read a new menu item name, but after we append the list to the 1st 
    # param list.
#index = dish names
#columns = nutrition headers (i.e. calories, fat, carbs, etc.)

# make data structure for each dish and iterate through ingredients and measurements until menu item != NaN (make sure to move past row index that has the name first)
#need to query opensearch


#TO DO
"""
- query opensearch for ingredients
# row ["INGREDIENTS"]
- calculate nutrition using opensearch and measurements and append to temp_l
- write back to excel
"""


#STEP 3
#Write back to an excel file
"""with pd.ExcelWriter('pandas_to_excel.xlsx') as writer:
    df.to_excel(writer, sheet_name='sheet1')
    df2.to_excel(writer, sheet_name='sheet2')"""

#df = dataframe to write to excel
