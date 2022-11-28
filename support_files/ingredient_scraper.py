"""
This program extracts the Carb information from Swathi's recipes.
The URL for this website is https://www.indianhealthyrecipes.com

Inputs to be given:
    main_url: The main page URL as given above
    food_item: The name of the food_item to be searched
    
Outputs of this program:
    carb_content_in_grams: The Carbohydrate content of the dish per serving in grams.
"""

import requests
from bs4 import BeautifulSoup
from psql.carb_info_db import create_tables, carb_info_db, update_carb_info_db

def carb_calc(
        main_url = "https://www.indianhealthyrecipes.com/",
        food_item = 'dosa'):
    
    if food_item == 'idli':
        food_item ='soft-idli'
    food_item += "-recipe"
    
    try:
        carb_content_in_grams = carb_info_db(food_item)
    except:
        create_tables()
        page=requests.get(f"{main_url}{food_item}")
        soup=BeautifulSoup(page.content, features="lxml")
        rows=soup.findAll("div",class_="nutrition-item nutrition-item-carbohydrates")
        carb_info = rows[0].find('span').text
        carb_content = carb_info.split()[1]
        carb_content_in_grams = float(carb_content[:-1])
        
        update_carb_info_db(food_item,carb_content_in_grams)
    return carb_content_in_grams
    

