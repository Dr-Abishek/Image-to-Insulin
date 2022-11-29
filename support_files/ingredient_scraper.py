"""
This program extracts the Carb information from Swasthi's recipes.
The URL for this website is https://www.indianhealthyrecipes.com

Inputs to be given:
    main_url: The main page URL as given above
    food_item: The name of the food_item to be searched
    
Outputs of this program:
    carb_content_in_grams: The Carbohydrate content of the dish per serving in grams.
"""

import requests
import streamlit as st
from bs4 import BeautifulSoup
from psql.carb_info_db import search_carb_info_db, update_carb_info_db

def carb_calc(
        main_url = "https://www.indianhealthyrecipes.com/",
        food_item = 'dosa'):
    
    food_id = None
    carb_content_in_grams = None
    if food_item == 'idli':
        food_item ='soft-idli'
    food_item += "-recipe"
    try:
        food_id, carb_content_in_grams = search_carb_info_db(food_item[:-7])
    except:
        if carb_content_in_grams is None:
            page=requests.get(f"{main_url}{food_item}")
            soup=BeautifulSoup(page.content, features="lxml")
            rows=soup.findAll("div",class_="nutrition-item nutrition-item-carbohydrates")
            carb_info = rows[0].find('span').text
            carb_content = carb_info.split()[1]
            carb_content_in_grams = float(carb_content[:-1])
            st.warning("Web scraping")
            food_id = update_carb_info_db(food_item[:-7],carb_content_in_grams)
        #st.warning("Error in getting carb information")
    finally:
        st.write(food_id, carb_content_in_grams)    
        return food_id, carb_content_in_grams
    

