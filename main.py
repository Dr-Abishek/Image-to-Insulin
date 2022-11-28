import streamlit as st
import i2i_calc
import pandas as pd

from psql.config import config
from psql.connect import connect
from psql.update_table import insert_info, insert_user
from psql.read_table import get_info, get_all_info, get_all_users
from psql.create_table import create_tables

# Title of the main page
st.title("Image-to-Insulin Calculator")
create_tables()
full_user_df = get_all_users()
user_id = None

def login():
  st.header("Login")
  user_id = int(st.number_input("Enter user id:",step=1))
  submit = st.button("Submit")
  if user_id is not None:
    try:
      if submit and (user_id in full_user_df['user_id']):
        f = open("user.txt", "w")
        f.write(str(user_id))
        f.close()
    except:
      st.write("User id not found. Please sign up")

def signup():
  
  form = st.form("Signup")
  st.table(full_user_df['email'])
  name = form.text_input("Enter your name:")
  email = form.text_input("Enter your email:")
  submit_state = form.form_submit_button("submit")
  if submit_state:
    if name== "" or email=="":
        st.warning("Please fill all fields")
    elif email in full_user_df['email']:
        st.warning("Email id already exists. Please enter another email")
    else:
        generated_id = insert_user(name,email)
        st.success(f"Successfully submitted. Your user id is {generated_id}")
        
def calc():
  try:    
    info = i2i_calc.app()
    
    if info is not None:
      f = open("info.txt", "w")
      f.write(info)
      f.close()
  except:
    st.write("Please log in with your user id first")
            
def dashboard():
  try:
    f0 = open("user.txt", "r"); user_id = f0.read(); f0.close();
    f1 = open("info.txt","r"); info = f1.read(); f1.close();
    
    st.header("Dashboard")
    
    if user_id is not None:
      df = get_info(user_id)
      st.table(df)
    logout = st.button("Logout")
    if logout:
      f0 = open("user.txt", "w"); f0.write(""); f0.close();
      f1 = open("info.txt","w"); f1.write(""); f1.close();
      user_id = None
      
  except:
    st.write("Please log in with your user id to access the dashboard")
  
  config()
  connect()
  
  
  
page = st.sidebar.selectbox('Select page',['Login','Signup','Calculate','Dashboard','Full Data'])
if page == 'Login':
    login()
elif page == 'Signup':
    signup()
elif page == 'Calculate':
    calc()
elif page == 'Dashboard':
    dashboard()
elif page == 'Full Data':
    full_info_df = get_all_info()
    if full_info_df is not None:
      st.table(full_info_df)
    if full_user_df is not None:
      st.table(full_user_df)
