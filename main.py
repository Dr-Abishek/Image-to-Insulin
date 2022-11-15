import streamlit as st
from yolov5.detect import run
import os
import yaml
import lxml
from ingredient_scraper import carb_calc
from get_item_codes import item_codes
#import pandas as pd


st.title("Image-to-Insulin calculator")
check = 0
final_list = []

##### PAGE 1
form1 = st.form("Upload")
form1.subheader("Upload your meal image to scan for food items")

image=form1.file_uploader("Please upload an image", type=['png','jpg','jpeg'], accept_multiple_files=False)
if image is not None:
    with open(os.path.join("yolov5/","temp_image.jpg"),"wb") as f: 
      f.write(image.getbuffer())         

f1_sb = form1.form_submit_button("Submit")
if f1_sb:
    st.write("Successfully submitted")
    check+=1
st.write(f"check = {check}")
    
######### Page 2
#Inference

txt_path = run(weights='last.pt', data = 'custom_data.yaml', source="yolov5/"+"temp_image.jpg") # Returns the path to the text file containing the results of the inference

item_codes_from_text = item_codes(txt_path)

#Infer the items according to item codes from the yaml file
st.markdown('---')
st.markdown("### Items Detected: ")
st.markdown("Please click the checkbox to confirm")

with open('custom_data.yaml') as file:
    try:
        qty=0
        databaseConfig = yaml.safe_load(file)
        item_names = databaseConfig.get('names')
        for item_code in item_codes_from_text:
            food_item = item_names[int(item_code)]
            option = st.checkbox(label=food_item,value=False)
            if option:
                qty = st.text_input("No. of servings of "+food_item,max_chars=3)
            if qty:
                final_list.append([food_item,qty])
            
    except yaml.YAMLError as exc:
        st.write(exc)
        
f2_sb = st.button("Submit")
if f2_sb:
    st.write("Successfully submitted")
    check+=1
    st.write(final_list)
st.write(f"check = {check}")

######### Page 3
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
