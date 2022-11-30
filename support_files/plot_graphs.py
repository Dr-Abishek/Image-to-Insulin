import matplotlib.pyplot as plt
import streamlit as st

def plot_graphs(df):
  col1,col2 = st.columns(2)
  
  fig1 = plt.figure()
  fig2 = plt.figure()
  ax1 = fig1.add_subplot(111)
  ax1.set_title("Carbs")
  ax2 = fig2.add_subplot(111)
  ax2.set_title("Insulin")
  
  ax1.hist(df[['carbs']])
  ax2.hist(df[['insulin']])
  
  col1.write(fig1)
  col2.write(fig2)
