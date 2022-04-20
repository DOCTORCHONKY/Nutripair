import nutrition_jason

fileName = "Jan's Health Bar (SAMPLE MENU).xlsx"
food_data = nutrition_jason.read_excel(fileName)
nutrition_jason.query_food('milk')
#nutrition_jason.calculate_nutrition(food_data)