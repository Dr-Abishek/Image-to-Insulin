import streamlit as st
from yolov5.detect import run
import os
import yaml
from ingredient_scraper import carb_calc


st.title("Image-to-Insulin calculator")
if "page" not in st.session_state:
    st.session_state.page = 0

def nextpage(): st.session_state.page += 1
def restart(): st.session_state.page = 0

placeholder = st.empty()
######## Page 1

st.subheader("Upload your meal image to scan for food items")

image=st.file_uploader("Please upload an image", type=['png','jpg','jpeg'], accept_multiple_files=False)
if image is not None:
    #Displaying image in the streamlit app once uploaded
    st.image(image)
    file_details = {"FileName":image.name,"FileType":image.type}
    st.write(file_details)
    
    with open(os.path.join("yolov5/","temp_image.jpg"),"wb") as f: 
      f.write(image.getbuffer())         
    #st.success("Saved File in yolov5/"+"temp_image.jpg")

submit_btn = st.button("Submit")
if submit_btn:
    st.write("Successfully submitted")
    nextpage()
    
######### Page 2
if st.session_state.page ==1:
    placeholder = st.empty()
    
    #Inference
    txt_path = run(weights='last.pt', data = 'custom_data.yaml', source="yolov5/"+"temp_image.jpg") # Returns the path to the text file containing the results of the inference
    
    #Read the ttext file and obtain the item codes
    #st.write(txt_path)
    f = open(txt_path+".txt", "r")
    text_result = f.read()
    item_codes_from_text = []
    list_from_text = text_result.split()
    for i in range(len(list_from_text)):
        code = int(float(list_from_text[i]))
        if float(list_from_text[i]) == code:
            if list_from_text[i] not in item_codes_from_text:
                item_codes_from_text.append(list_from_text[i])
    #st.write(type(item_codes_from_text))
    
    
    #Infer the items according to item codes from the yaml file
    st.markdown('---')
    st.markdown("### Items Detected: ")
    st.markdown("Please click the checkbox to confirm")
    food_item_qty_dict = {}
    with open('custom_data.yaml') as file:
        try:
            databaseConfig = yaml.safe_load(file)
            item_names = databaseConfig.get('names')
            for item_code in item_codes_from_text:
                food_item = item_names[int(item_code)]
                option = st.checkbox(label=food_item,value=True)
                if option:
                    qty = st.text_input("No. of servings of "+food_item,max_chars=3)
                    food_item_qty_dict[food_item] = qty
                    
        except yaml.YAMLError as exc:
            st.write(exc)
    st.write(food_item_qty_dict)
    
    confirm_btn = st.button("Confirm to Submit")
    if confirm_btn:
        nextpage()
    

######### Page 3
if st.session_state.page == 2:
    pg_3 = st.empty()
    
    sugar_level_offset=0
    blood_sugar_prior_meal = pg_3.text_input("Enter your blood sugar prior to the meal",max_chars=3)
    pg_3.write("Assuming a normal blood sugar level of 120..."
    if blood_sugar_prior_meal != '':
        sugar_level_offset=int(blood_sugar_prior_meal)-120
