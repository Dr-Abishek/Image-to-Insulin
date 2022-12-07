import matplotlib.pyplot as plt
import streamlit as st

def plot_graphs(df):
  col1,col2 = st.columns(2)
  df = df.set_index('date')
  
  fig1 = plt.figure()
  df['carbs'].plot(kind='bar')
  plt.title("Carbs")
  
  
  fig2 = plt.figure()
  df['insulin'].plot(kind='bar')
  plt.title("Insulin")
  #ax1 = fig1.add_subplot(111)
  #ax1.set_title("Carbs")
  #ax2 = fig2.add_subplot(111)
  #ax2.set_title("Insulin")
  
  #
  
  #ax1.barh(df['date'],df['carbs'])
  #ax2.barh(df['date'],df['insulin'],color = 'red')
  
  col1.write(fig1)
  col2.write(fig2)
