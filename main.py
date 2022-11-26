import streamlit as st

# Custom imports 
from multipage import MultiPage
import login, i2i_calc, dashboard # import your pages here

# Create an instance of the app 
app = MultiPage()

# Title of the main page
st.title("Data Storyteller Application")

# Add all your applications (pages) here
app.add_page("Login/Signup", login.app)
app.add_page("Image-to-Insulin Calculator", i2i_calc.app)
app.add_page("Dashboard", dashboard.app)


# The main app
app.run()
