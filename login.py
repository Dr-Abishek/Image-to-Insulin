import streamlit as st
def login_app():
  st.title("Login")
  user_id = int(st.number_input("Enter user id:"))
  submit = st.button("Submit")
  if user_id is not None:
    try:
      if submit is not None:
        return user_id
    except:
      st.write("User id not found. Please sign up")
  
