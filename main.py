import streamlit as st
from yolov5.detect import run
import os
import yaml



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
    st.write(txt_path)
    f = open(txt_path+".txt", "r")
    text_result = f.read()
    item_codes_from_text = []
    list_from_text = text_result.split()
    for i in range(len(list_from_text)):
        code = int(float(list_from_text[i]))
        if float(list_from_text[i]) == code:
            if list_from_text[i] not in item_codes_from_text:
                item_codes_from_text.append(list_from_text[i])
    st.write(item_codes_from_text)
    
    
    #Infer the items according to item codes from the yaml file
    with open('custom_data.yaml') as file:
        try:

            databaseConfig = yaml.safe_load(file)   
            print(databaseConfig)
        except yaml.YAMLError as exc:
            print(exc)

    
    
