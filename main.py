import streamlit as sl
!git clone https://github.com/ultralytics/yolov5  # clone
# %cd yolov5
# %pip install -qr requirements.txt  # install

import torch
import utils

sl.title("Image-to-Insulin calculator")
sl.subheader("Upload your meal image to scan for food items")

image=sl.file_uploader("Please upload an image", type=['png','jpg','jpeg'], accept_multiple_files=False)
if image is not None:
    #Displaying image in the streamlit app once uploaded
    sl.image(image)

submit_btn = sl.button("Submit")
if submit_btn:
    sl.write("Successfully submitted")
