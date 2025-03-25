# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col


name_on_order = st.text_input("Name on smoothie:")
st.write("The name on your smoothie will be", name_on_order)

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write("Choose the fruits you want in your custom smoothie!")

#option = st.selectbox( "What is your favorite fruit?",("Banana", "Strawberries", "Peaches"),)

#st.write("Your favorite fruit is :", option)



session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select (col('fruit_name'))
st.dataframe(data=my_dataframe, use_container_width=True)




options = st.multiselect(
    "Choose up to 5 ingredients: ",my_dataframe,max_selections=5
    
)
if options:
    #st.write("You selected:", options)
    ingredients_string = ''
    for x in options:
        ingredients_string += x + ' '
        #st.write(ingredients_string)
        
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','"""+name_on_order+"""')"""

    #st.write(my_insert_stmt)
    time_to_insert = st.button('Submit Order',use_container_width=True)

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")

    st.stop()
