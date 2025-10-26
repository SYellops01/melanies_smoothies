# Import python packages
import streamlit as st
import requests
#import column function to pull specific column from dataframe
from snowflake.snowpark.functions import col



# Write directly to the app
st.title(f"Customize Your Smoothie! :cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom Smoothie!
  """
)

name_on_order=st.text_input('Please enter your name for this order: ')

#Set session and dataframe to pull fruit name from table in database
cnx=st.connection("snowflake")
session=cnx.session()
my_dataframe=session.table("smoothies.public.fruit_options").select(col('SEARCH_ON'))

#create multi-select button to choose ingredients.Impose max 5 selections on user
ingredients_list=st.multiselect("Choose up to 5 ingredients: ", my_dataframe, max_selections=5)
#When more than one ingredient is selected, build order
if len(ingredients_list)>0:
    ingredients_string=''
    for fruits_chosen in ingredients_list:
        ingredients_string +=fruits_chosen + ', '
        #pull nutritional information for each fruit chosen
        st.subheader(fruits_chosen+' Nutrition Information')
        smoothiefroot_response=requests.get("https://my.smoothiefroot.com/api/fruit/"+fruits_chosen)
        sf_df=st.dataframe(data=smoothiefroot_response.json(),use_container_width=True)
    ingredients_string=ingredients_string[:len(ingredients_string)-2]
    
    #st.write(ingredients_string)

    #statement to insert into the table
    my_insert_statement="""insert into smoothies.public.orders(ingredients,name_on_order)
    values 
    ('""" +ingredients_string+"""','""" + name_on_order + """')"""

    #add submit button to submit order
    time_to_insert=st.button('Submit Order')
    
    if time_to_insert:
        session.sql(my_insert_statement).collect()
        st.success('Your Smoothie is ordered, '+name_on_order+'!',icon="✅")



