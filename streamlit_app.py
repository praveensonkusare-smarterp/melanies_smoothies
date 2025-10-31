
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title("Customize your smoothie!")
st.write("Choose the fruits you want in your custom Smoothie!")


name_on_order = st.text_input("Name of Smoothie:")
st.write("The name of your soomthie will be:", name_on_order)

# Get active Snowflake session
session = get_active_session()

# Fetch fruit options
my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"))
fruit_list = [row["FRUIT_NAME"] for row in my_dataframe.collect()]

# Multi-select input
ingredients_list = st.multiselect("Choose up to 5 ingredients:", fruit_list)

if ingredients_list and name_on_order:
    if len(ingredients_list) > 5:
        st.error("Please select only up to 5 ingredients.")
    else:
        # Create a comma-separated string of fruits
        ingredients_string = ", ".join(ingredients_list)

        # Insert into Snowflake
        my_insert_stmt = f"""
            INSERT INTO smoothies.public.orders(ingredients,name_on_order)
            VALUES ('{ingredients_string}','{name_on_order}')
        """
        time_to_insert = st.button('Submit Order')

        if time_to_insert:

        # Execute the insert
            session.sql(my_insert_stmt).collect()

        # Show success message
            st.success("Your Smoothie is ordered!", icon="✅")


        
