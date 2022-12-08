import streamlit as st
import i2i_calc
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from PIL import Image
from psql.config import config
from psql.connect import connect
from psql.update_table import insert_info, insert_user
from psql.read_table import get_info, get_all_info, get_all_users, get_all_carbs
from psql.create_table import create_tables
from support_files.plot_graphs import plot_graphs
from support_files.get_model_and_labels import download_blob_from_azure, upload_blob_to_azure


from datetime import date, timedelta
today = date.today()

# Title of the main page
st.title("Image-to-Insulin Calculator")
#create_tables()
full_user_df = get_all_users()


def login():
  st.header("Login")
  user_id = int(st.number_input("Enter user id:",step=1))
  submit = st.button("Submit")
  if user_id is not None:
    try:
      if submit and (user_id in full_user_df.values):
        f = open("user.txt", "w")
        f.write(str(user_id))
        f.close()
        st.success('Login Successful')
      else:
        st.warning("User id not found. Please sign up")
    except:
      st.warning("User id not found. Please sign up")

      
      
def signup():
  form = st.form("Signup")
  name = form.text_input("Enter your name:")
  email = form.text_input("Enter your email:")
  submit_state = form.form_submit_button("submit")
  if submit_state:
    if name== "" or email=="":
        st.warning("Please fill all fields")
    elif email in full_user_df.values:
        st.warning("Email id already exists. Please enter another email")
    else:
        st.write("Generating user id...")
        generated_id = insert_user(name,email)
        
        #Pre-generating images and text files for new user
        temp_str = "Temp"
        image = Image.open('support_files/smiley.jpg')
        upload_blob_to_azure(blob = image,type_of_blob = "img",user_id = int(generated_id))
        upload_blob_to_azure(blob = temp_str, type_of_blob = "txt", user_id = int(generated_id))
        upload_blob_to_azure(blob = temp_str, type_of_blob = "txt2", user_id = int(generated_id))
        
        st.success(f"Successfully submitted. Your user id is {generated_id}")

        
def calc():
  #try:
  
  user_id = ""
  
  f0 = open("user.txt", "r"); user_id = f0.read(); f0.close();
  st.success(f"User ID: {user_id}")
  if user_id !="" and user_id is not None:
    info = None
    info = i2i_calc.app(user_id)
    if (info is not None):
      info_list = info.split(',')
      total_carbs_in_meal = info_list[-2]
      avg_insulin_per_item_in_meal = float(info_list[-1])

      food_info = np.array(info_list[:-2])
      no_of_items = int(len(food_info)/3)
      reshaped_food_info = np.reshape(food_info,(no_of_items,3))#.T
      #st.table(reshaped_food_info)

      for row in reshaped_food_info:
        food = row[0]
        carbs = float(row[2])
        insert_info(today,food,carbs,avg_insulin_per_item_in_meal/no_of_items,user_id)

  else:
    st.write("Please log in with your user id first")
            
def dashboard():
  #try:
    user_id = ""
    f0 = open("user.txt", "r"); user_id = f0.read(); f0.close();
    
    st.header("Dashboard")
    st.success(f"User-id: {user_id}")
    if user_id != "":
      df = get_info(user_id)
      #columns: date, food carbs, insulin
      
      opt=st.sidebar.radio("Choose time frame for viewing stats.", options=("day",'week','month','year'))
      
      if opt == 'day':
        df_day = df[df['date'] == today]
        #st.table(df_day)
        plot_graphs(df_day)
        st.markdown("---")
        st.markdown(f"#### Total carbs consumed for today: {sum(df_day['carbs'])}")
        st.markdown(f"#### Total insulin dosage for today: {sum(df_day['insulin'])}")
        st.markdown("---")
        
      elif opt =='week':
        day_of_week = today.weekday()
        week_start = date.today() - timedelta(days = day_of_week)
        week_end = week_start + timedelta(days = 6)
        df_week = df[(df['date'] >= week_start) & (df['date'] <= week_end)]
        #st.table(df_week)                                                
        plot_graphs(df_week)
        st.markdown("---")
        st.markdown(f"#### Total carbs consumed for this week: {sum(df_week['carbs'])}")
        st.markdown(f"#### Total insulin dosage for this week: {sum(df_week['insulin'])}")
        st.markdown("---")
        
      elif opt == 'month':
        df_month = df.copy()
        df_month['date'] = pd.to_datetime(df_month['date'], format='%Y-%m-%d')
        df_month = df_month[df_month['date'].dt.strftime('%Y-%m') == today.strftime('%Y-%m')]
        #st.table(df_month)
        plot_graphs(df_month)
        st.markdown("---")
        st.markdown(f"#### Total carbs consumed for this month: {sum(df_month['carbs'])}")   
        st.markdown(f"#### Total insulin dosage for this month: {sum(df_month['insulin'])}")
        st.markdown("---")
        
      elif opt =='year':
        df_year = df.copy()
        df_year['date'] = pd.to_datetime(df_year['date'], format='%Y-%m-%d')
        df_year = df_year[df_year['date'].dt.strftime('%Y') == today.strftime('%Y')]
        #st.table(df_year)
        plot_graphs(df_year)
        st.markdown("---")
        st.markdown(f"#### Total carbs consumed for this year: {sum(df_year['carbs'])}")
        st.markdown(f"#### Total insulin dosage for this year: {sum(df_year['insulin'])}")
        st.markdown("---")
      
      logout = st.button("Logout")
      if logout:
        f0 = open("user.txt", "w"); f0.write(""); f0.close();
        #f1 = open("info.txt","w"); f1.write(""); f1.close();
        user_id = None
    else:
      st.write("Please log in with your user id to access the dashboard")
    
  #except:
    #st.write("Please log in with your user id to access the dashboard")
  
  
  
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
    #full_info_df = get_all_info()
    full_carb_df = get_all_carbs()
    #if full_info_df is not None:
      #st.table(full_info_df)
    if full_user_df is not None:
      st.table(full_user_df)
    if full_carb_df is not None:
      st.table(full_carb_df)
