import streamlit as st
import i2i_calc

# Title of the main page
st.title("Image-to-Insulin Calculator")
def nextpage(): st.session_state.count += 1
def restart(): st.session_state.count = 1

user_id = None
st.markdown(user_id)
def login():
  st.header("Login")
  user_id = int(st.number_input("Enter user id:",step=1))
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
  if user_id is not None:
    final_list_2, total_carbs_in_meal, recommended_insulin = i2i_calc.app()
  else:
    st.write("Please log in with your user id first")
            
def dashboard():
  if user_id is not None:
    st.header("Dashboard")
  else:
    st.write("Please log in with your user id first")
  

page = st.sidebar.selectbox('Select page',['Login','Signup','Calculate','Dashboard'])
if page == 'Login':
    user_id = login()
elif page == 'Signup':
    signup()
elif page == 'Calculate':
    calc()
elif page == 'Dashboard':
    dashboard()
