import streamlit as st
from yolov5.detect import run
import os
import yaml
import lxml
from ingredient_scraper import carb_calc
from get_item_codes import item_codes
from read_yaml import Read_Yaml
#import pandas as pd

final_list = []
st.title("Image-to-Insulin calculator")
if 'count' not in st.session_state:
    st.session_state.count = 0

def nextpage(): st.session_state.count += 1
def restart(): st.session_state.count = 0

placeholder = st.empty()
st.button("Next",on_click=nextpage,disabled=(st.session_state.count > 3))

##### PAGE 1
if st.session_state.count == 0:
    #form1 = placeholder.form("Upload")
    with placeholder.container():
        st.subheader("Upload your meal image to scan for food items")

        image=st.file_uploader("Please upload an image", type=['png','jpg','jpeg'], accept_multiple_files=False)
        if image is not None:
            with open(os.path.join("yolov5/","temp_image.jpg"),"wb") as f: 
              f.write(image.getbuffer())         
    
######### Page 2

elif st.session_state.count == 1:
    #Inference
    with placeholder.container():
        st.write("Detecting food items..." )
        txt_path = run(weights='last.pt', data = 'custom_data.yaml', source="yolov5/"+"temp_image.jpg") # Returns the path to the text file containing the results of the inference
        item_codes_from_text = item_codes(txt_path)
        st.write("item_codes_from_text:")
        st.write(item_codes_from_text)

        f = open("temp.txt", "w")
        for item_codes in item_codes_from_text:
            f.write(str(item_codes)+"\t")
        f.close()
######### Page 3 
elif st.session_state.count == 2:
    #Infer the items according to item codes from the yaml file
    with placeholder.container():
        st.markdown('---')
        st.write("Items Detected: ")
        st.write("Please click the checkbox to confirm")

        f0 = open("temp.txt", "r")
        item_codes_from_text = f0.read().split()
        st.write("item_codes_from_text:")
        st.write(item_codes_from_text)
        #final_list = Read_Yaml(item_codes_from_text)
        
        with open('custom_data.yaml') as file:
            try:
                qty=0
                databaseConfig = yaml.safe_load(file)
                item_names = databaseConfig.get('names')
                st.write("item_names:")
                st.write(item_names)
                for item_code in item_codes_from_text:
                    food_item = item_names[int(item_code)]
                    option = st.checkbox(label=food_item,value=True)
                    qty = st.text_input("No. of servings of "+food_item,max_chars=3)
                    #if option and qty:
                    final_list.append([food_item,qty])

            except yaml.YAMLError as exc:
                st.write(exc)
        f0.close()

        st.write("final_list")
        st.write(final_list)

        f1 = open("temp.txt", "w")
        for row in final_list:
            for item in row:
                f1.write('%s\t' %item)
            f1.write('\n')
        f1.close()
        

######### Page 4
elif st.session_state.count == 3:
    with placeholder.container():
        f2 = open("temp.txt", "r")
        st.write(f2.read())
        #placeholder.write(final_list)
        st.markdown('---')
        sugar_level_offset=0

        blood_sugar_prior_meal = placeholder.text_input("Enter your blood sugar prior to the meal",max_chars=3)

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
            st.markdown("### Your recommended Insulin Dosage as per the [Healthline website](https://www.healthline.com/health/how-much-insulin-to-take-chart#how-to-calculate) is "+str(recommended_insulin)+" units")

else:
    with placeholder.container():
        st.write("This is the end")
        st.button("Restart",on_click=restart) 
