import streamlit as st
from yolov5.detect import run
import os
import yaml
import lxml
from ingredient_scraper import carb_calc
from get_item_codes import item_codes
from read_yaml import Read_Yaml
#import pandas as pd


st.title("Image-to-Insulin calculator")
if "page" not in st.session_state:
    st.session_state.page = 0

def nextpage(): st.session_state.page += 1
def restart(): st.session_state.page = 0

placeholder = st.empty()
st.button("Next",on_click=nextpage,disabled=(st.session_state.page > 3))

final_list = []

##### PAGE 1
if st.session_state.page == 0:
    #form1 = placeholder.form("Upload")
    placeholder.subheader("Upload your meal image to scan for food items")

    image=placeholder.file_uploader("Please upload an image", type=['png','jpg','jpeg'], accept_multiple_files=False)
    if image is not None:
        with open(os.path.join("yolov5/","temp_image.jpg"),"wb") as f: 
          f.write(image.getbuffer())         
    
######### Page 2

elif st.session_state.page == 1:
    #Inference

    txt_path = run(weights='last.pt', data = 'custom_data.yaml', source="yolov5/"+"temp_image.jpg") # Returns the path to the text file containing the results of the inference

    item_codes_from_text = item_codes(txt_path)

    #Infer the items according to item codes from the yaml file
    placeholder.markdown('---')
    placeholder.markdown("### Items Detected: ")
    placeholder.markdown("Please click the checkbox to confirm")

    final_list = Read_Yaml(item_codes_from_text)


    #
   
######### Page 3
elif st.session_state.page == 2:
    st.write(final_list)
    st.markdown('---')
    sugar_level_offset=0

    blood_sugar_prior_meal = st.text_input("Enter your blood sugar prior to the meal",max_chars=3)

    if blood_sugar_prior_meal != '':
        st.write("Assuming a normal blood sugar level of 120...")
        sugar_level_offset=float(blood_sugar_prior_meal)-120

    total_carbs_in_meal = 0

    for row in final_list:
        food = row[0]
        qty = row[1]
        total_carbs_in_meal += int(qty)*carb_calc(food_item=food)
    st.write("Total carbs in your meal, as calculated by scraping [Swasthi's Recipes] (https://www.indianhealthyrecipes.com/) is "+str(total_carbs_in_meal) + "g")
    recommended_insulin = round(( (sugar_level_offset/50) + (total_carbs_in_meal) /10) *2.0)/2.0

    if recommended_insulin:
        st.markdown("## Your recommended Insulin Dosage as per the [Healthline website](https://www.healthline.com/health/how-much-insulin-to-take-chart#how-to-calculate) is "+str(recommended_insulin)+" units")
