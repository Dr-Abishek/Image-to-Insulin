import streamlit as st
import i2i_calc

# Title of the main page
st.title("Image-to-Insulin Calculator")
def nextpage(): st.session_state.count += 1
def restart(): st.session_state.count = 1

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
  st.header("Signup")
  
def calc():
  try:
    f = open("user.txt", "r")
    user_id = f.read()
    f.close()
    
    info = i2i_calc.app()
    st.write(info)
    if info is not None:
      f = open("info.txt", "w")
      f.write(info)
      f.close()
  except:
    st.write("Please log in with your user id first")
            
def dashboard():
  try:
    f = open("user.txt", "r")
    user_id = f.read()
    f.close()
    st.header("Dashboard")
  except:
    st.write("Please log in with your user id first")
  

page = st.sidebar.selectbox('Select page',['Login','Signup','Calculate','Dashboard'])
if page == 'Login':
    login()
elif page == 'Signup':
    signup()
elif page == 'Calculate':
    calc()
elif page == 'Dashboard':
    dashboard()
st.markdown(user_id)
