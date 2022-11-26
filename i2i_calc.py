
import streamlit as st
from yolov5.detect import run
import os
import yaml
import lxml
import numpy as np
from support_files.ingredient_scraper import carb_calc
from support_files.get_item_codes import item_codes
from support_files.read_yaml import Read_Yaml
#import pandas as pd

final_list = []
final_list_2 = []
st.title("Image-to-Insulin calculator")
if 'count' not in st.session_state:
    st.session_state.count = 1

def nextpage(): st.session_state.count += 1
def restart(): st.session_state.count = 1

placeholder = st.empty()
st.button("Next",on_click=nextpage,disabled=(st.session_state.count > 4))


        
##### PAGE 1
if st.session_state.count == 1:
    
    # Upload Image for Inference
    with placeholder.container():
        st.subheader("Upload your meal image to scan for food items")

        image=st.file_uploader("Please upload an image", type=['png','jpg','jpeg'], accept_multiple_files=False)
        if image is not None:
            st.image(image)
            with open(os.path.join("yolov5/","temp_image.jpg"),"wb") as f: 
              f.write(image.getbuffer())         
    
######### Page 2

elif st.session_state.count == 2:
    #Inference
    with placeholder.container():
        st.write("Detecting food items..." )
        txt_path = run(weights='last.pt', data = 'custom_data.yaml', source="yolov5/"+"temp_image.jpg") # Returns the path to the text file containing the results of the inference
        item_codes_from_text = item_codes(txt_path)
        st.write("Click 'Next' to see detected items")
        
        f = open("temp.txt", "w")
        for item_code in item_codes_from_text:
            f.write(str(item_code)+"\t")
        f.close()
        
        
######### Page 3 
elif st.session_state.count == 3:
    #Infer the items according to item codes from the yaml file
    with placeholder.container():
        st.markdown('---')
        st.write("Items Detected: ")
        st.write("Please click the checkbox to confirm the detected items.")
        st.write("The detected serving quantities are displayed in the text box below the food item. You can change it as necessary") 
        
        f0 = open("temp.txt", "r")
        item_codes_from_text = f0.read().split()
        #st.write(item_codes_from_text)
        unique_item_codes, frequency = np.unique(item_codes_from_text, return_counts = True)
        with open('custom_data.yaml') as file:
            try:
                qty=0
                databaseConfig = yaml.safe_load(file)
                item_names = databaseConfig.get('names')
                for i in range(len(unique_item_codes)):
                    food_item = item_names[int(unique_item_codes[i])]
                    option = st.checkbox(label=food_item,value=True)
                    qty = st.number_input("No. of servings of "+food_item,value=float(frequency[i]),step=0.5)
                    if option and qty:
                        final_list.append([food_item,qty])

            except yaml.YAMLError as exc:
                st.write(exc)
        f0.close()
        
        radio = st.radio(label = "Any other items that failed to get detected or are detected wrongly?",options=['No','Yes'])
        if radio == 'Yes':
            no_of_missing_items = st.number_input("How many such items?",value=1,step=1)

            for m in range(no_of_missing_items):
                food_item_new = st.text_input("Food item: ",key=str(m))
                qty_new = st.number_input("No. of servings: ",value=1.0,step=0.5, key=str(-m-1))
                food_item_new = food_item_new.replace(" ","-")
                final_list.append([food_item_new,qty_new])
        
        #st.write("final_list")
        #st.write(final_list)

        f1 = open("temp1.txt", "w")
        for row in final_list:
            for item in row:
                f1.write('%s\t' %item)
            f1.write('\n')
        f1.close()
        

######### Page 4
elif st.session_state.count == 4:
    with placeholder.container():
        #Display all the info as of now till here....
        
        f2 = open("temp1.txt", "r")
        lines = f2.readlines()
        for line in lines:
            final_list_2.append(line.split())
        st.markdown('---')
        sugar_level_offset=0
        
       
        blood_sugar_prior_meal = st.number_input("Enter your blood sugar prior to the meal",value=0,step=1)

        if blood_sugar_prior_meal != 0:
            st.write("Assuming a normal blood sugar level of 120...")
            sugar_level_offset=float(blood_sugar_prior_meal)-120

            total_carbs_in_meal = 0

            for row in final_list_2:
                food = row[0]
                qty = float(row[1])
                #st.write("food: "+str(food)+", qty: "+str(qty))
                total_carbs_in_meal += qty*carb_calc(food_item=food)
            st.write("Total carbs in your meal, as calculated by scraping [Swasthi's Recipes](https://www.indianhealthyrecipes.com/) is "+str(total_carbs_in_meal) + "g")
            recommended_insulin = round(( (sugar_level_offset/50) + (total_carbs_in_meal) /10) *2.0)/2.0

            if recommended_insulin:
                st.markdown("### Your recommended Insulin Dosage as per the [Healthline website](https://www.healthline.com/health/how-much-insulin-to-take-chart#how-to-calculate) is "+str(recommended_insulin)+" units")

else:
    with placeholder.container():
        st.write("This is the end")
        st.button("Restart",on_click=restart) 