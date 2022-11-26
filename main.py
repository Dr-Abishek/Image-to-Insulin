import streamlit as st
import i2i_calc
from psql.config import config
from psql.connect import connect

# Title of the main page
st.title("Image-to-Insulin Calculator")

user_id = None

def login():
  st.header("Login")
  user_id = int(st.number_input("Enter user id:",step=1))
  submit = st.button("Submit")
  if user_id is not None:
    try:
      if submit is not False:
        f = open("user.txt", "w")
        f.write(str(user_id))
        f.close()
    except:
      st.write("User id not found. Please sign up")

def signup():
  form = st.form("Signup")
  name = form.text_input("Enter your name:")
  email = form.text_input("Enter your email:")
  submit_state = form.form_submit_button("submit")
  if submit_state:
    if name== "" or email=="":
        st.warning("Please fill all fields")
    else:
        st.success("Successfully submitted")
        
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
      st.write(user_id)
      st.write(info)
    logout = st.button("Logout")
    if logout:
      f0 = open("user.txt", "w"); f0.write(""); f0.close();
      f1 = open("info.txt","w"); f1.write(""); f1.close();
      user_id = None
      
  except:
    st.write("Please log in with your user id to access the dashboard")
  
  config()
  connect()

page = st.sidebar.selectbox('Select page',['Login','Signup','Calculate','Dashboard'])
if page == 'Login':
    login()
elif page == 'Signup':
    signup()
elif page == 'Calculate':
    calc()
elif page == 'Dashboard':
    dashboard()

