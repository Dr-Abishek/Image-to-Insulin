import streamlit as st
from yolov5.detect import run

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

submit_btn = st.button("Submit")
if submit_btn:
    st.write("Successfully submitted")
    nextpage()
    
######### Page 2
if st.session_state.page ==1:
    run()


    
    
