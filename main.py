import streamlit as st
from yolov5.detect import run
import os
import yaml
import lxml
import numpy as np
from support_files.ingredient_scraper import carb_calc
from support_files.get_item_codes import item_codes
from support_files.read_yaml import Read_Yaml
import i2i_calc
#import pandas as pd

# Title of the main page
st.title("Image-to-Insulin Calculator")
def nextpage(): st.session_state.count += 1
def restart(): st.session_state.count = 1

def login():
  st.header("Login")
  user_id = int(st.number_input("Enter user id:"))
  submit = st.button("Submit")
  if user_id is not None:
    try:
      if submit is not None:
        return user_id
    except:
      st.write("User id not found. Please sign up")

def signup():
  st.header("Signup")
  
def calc():
  final_list_2, total_carbs_in_meal, recommended_insulin = i2i_calc.app()
            
def dashboard():
  st.header("Dashboard")

page = st.sidebar.selectbox('Select page',['Login','Signup','Calculate','Dashboard'])
if page == 'Login':
    user_id = login()
elif page == 'Signup':
    signup()
elif page == 'Calculate':
    calc()
elif page == 'Dashboard':
    dashboard()
