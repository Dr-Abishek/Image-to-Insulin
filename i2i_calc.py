import streamlit as st
from yolov5.detect import run
import os
import yaml
import lxml
import numpy as np
#import PIL
#from PIL import Image 
from support_files.ingredient_scraper import carb_calc
from support_files.get_item_codes import item_codes
from support_files.read_yaml import Read_Yaml
from support_files.get_model_and_labels import download_blob_from_azure, upload_blob_to_azure


def nextpage(): st.session_state.count += 1
def restart(): st.session_state.count = 1

def app(user_id):
    final_list = []
    final_list_2 = []
    #st.title("Image-to-Insulin calculator")
    if 'count' not in st.session_state:
        st.session_state.count = 1
    placeholder = st.empty()
    st.button("Next",on_click=nextpage,disabled=(st.session_state.count > 4))
    
    ##### PAGE 1 ####### Upload Image for Inference ##########################
    
    if st.session_state.count == 1:
            
        with placeholder.container():
            st.subheader("Welcome to the image-to-insulin app")
            st.subheader("Upload your meal image to scan for food items")

            image=st.file_uploader("Please upload an image", type=['png','jpg','jpeg'], accept_multiple_files=False)
            if image is not None:
                st.image(image)
                try:
                    upload_blob_to_azure(blob = image,type_of_blob = "img",user_id = user_id)
                    st.success("Uploaded image successfully")
                except:
                    st.warning("Blob upload unsuccessful")
        

    ######### Page 2 ###### Inference ########################################

    elif st.session_state.count == 2:
        
        with placeholder.container():
            st.write("Downloading model & labels for inference..." )
            try:
                download_blob_from_azure(['custom_data.yaml','last.pt'])
                download_blob_from_azure(["temp_img_"+str(user_id)+".jpg"])
            except:
                st.warning("Blob retrieval unsuccessful")
            st.write("Detecting food items..." )
            
            txt_path = run(weights='last.pt', data = 'custom_data.yaml', source="temp_img_"+str(user_id)+".jpg") # Returns the path to the text file containing the results of the inference
            item_codes_from_text = item_codes(txt_path)
            st.write("Click 'Next' to see detected items")

            #f = open("temp.txt", "w")
            #for item_code in item_codes_from_text:
                #f.write(str(item_code)+"\t")
            #f.close()
            temp_str = ""
            for item_code in item_codes_from_text:
                temp_str += str(item_code)+"\t"
            upload_blob_to_azure(blob = temp_str,type_of_blob = "txt",user_id = user_id)

    ######### Page 3 ##### Infer the items according to item codes########
    
    elif st.session_state.count == 3:
        
        with placeholder.container():
            st.markdown('---')
            st.subheader("Items Detected: ")
            st.write("Please click the checkbox to confirm the detected items.")
            st.write("The detected serving quantities are displayed in the text box below the food item. You can change it as necessary") 
            
            try:
                download_blob_from_azure(["temp_txt_"+str(user_id)+".txt"])
                download_blob_from_azure(['custom_data.yaml'])
            except:
                st.warning("Blob retrieval unsuccessful")
            
            f0 = open("temp_txt_"+str(user_id)+".txt", "r")
            item_codes_from_text = f0.read().split()
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
            st.warning("""Please press the 'Enter' key after inputting the blood sugar. 
                       Once the recommended insulin dosage is displayed, you may click on 'Next'.""")
            if blood_sugar_prior_meal != 0:
                st.write("Assuming a normal blood sugar level of 120...")
                sugar_level_offset=float(blood_sugar_prior_meal)-120

                total_carbs_in_meal = 0
                return_string = ""

                for row in final_list_2:
                    food = row[0]
                    qty = float(row[1])
                    item_carb = carb_calc(food_item=food)[1]
                    return_string += str(food)+","+str(qty)+","+str(item_carb)+","
                    total_carbs_in_meal += qty*item_carb
                    
                st.write("Total carbs in your meal is "+str(total_carbs_in_meal) + "g")
                recommended_insulin = round(( (sugar_level_offset/50) + (total_carbs_in_meal) /10) *2.0)/2.0

                if recommended_insulin:
                    st.markdown("### Your recommended Insulin Dosage as per the [Healthline website](https://www.healthline.com/health/how-much-insulin-to-take-chart#how-to-calculate) is "+str(recommended_insulin)+" units")
                    return return_string + str(total_carbs_in_meal) + "," +str(recommended_insulin)
    else:
        with placeholder.container():
            st.write("This is the end. Please click on restart to calculate from another image.")
            st.button("Restart",on_click=restart) 
