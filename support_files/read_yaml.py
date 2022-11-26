import streamlit as st
import yaml

def Read_Yaml(item_codes_from_text):
  final_list = []
  with open('custom_data.yaml') as file:
    try:
        qty=0
        databaseConfig = yaml.safe_load(file)
        item_names = databaseConfig.get('names')
        for item_code in item_codes_from_text:
            food_item = item_names[int(item_code)]
            option = st.checkbox(label=food_item,value=False)
            if option:
                qty = st.text_input("No. of servings of "+food_item,max_chars=3)
            if qty:
                final_list.append([food_item,qty])
            
    except yaml.YAMLError as exc:
        st.write(exc)
  return(final_list)
    
