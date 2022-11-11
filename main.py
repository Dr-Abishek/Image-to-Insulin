import streamlit as st

st.title("Image-to-Insulin calculator")

######## Page 1

st.subheader("Upload your meal image to scan for food items")

image=st.file_uploader("Please upload an image", type=['png','jpg','jpeg'], accept_multiple_files=False)
if image is not None:
    #Displaying image in the streamlit app once uploaded
    st.image(image)

submit_btn = st.button("Submit")
if submit_btn:
    st.write("Successfully submitted")
