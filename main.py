import streamlit as st
from yolov5.detect import run
import os


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
    st.success("Saved File in yolov5/"+"temp_image.jpg")

submit_btn = st.button("Submit")
if submit_btn:
    st.write("Successfully submitted")
    nextpage()
    
######### Page 2
if st.session_state.page ==1:
    placeholder = st.empty()
    txt_path = run(weights='last.pt',source="yolov5/"+"temp_image.jpg")
    st.write(txt_path)
    f = open(txt_path+".txt", "r")
    text_result = f.read()
    list_from_text = text_result.split()
    for i in range(len(list_from_text)):
        st.write(list_from_text[i])



    
    
