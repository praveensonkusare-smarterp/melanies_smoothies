import streamlit as st
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title("Customize your smoothie!")
st.write("Choose the fruits you want in your custom Smoothie!")

name_on_order = st.text_input("Name of Smoothie:")
st.write("The name of your smoothie will be:", name_on_order)

# Get active Snowflake session
cnx = st.connection("snowflake")
session = cnx.session()

# Fetch fruit options
my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"))
fruit_list = [row["FRUIT_NAME"] for row in my_dataframe.collect()]

# Multi-select input
ingredients_list = st.multiselect("Choose up to 5 ingredients:", fruit_list)

# Only continue if user has selected ingredients and entered a name
if ingredients_list and name_on_order:
    if len(ingredients_list) > 5:
        st.error("Please select only up to 5 ingredients.")
    else:
        # -----------------------------
        # WORKSHOP-CORRECT VERSION
        # Build the string manually with spaces (no commas)
        # Includes trailing space
        # -----------------------------
        ingredients_string = ""

        for fruit_chosen in ingredients_list:
            ingredients_string += fruit_chosen + " "

        # Build SQL INSERT just like the workshop
        my_insert_stmt = """
            INSERT INTO smoothies.public.orders(ingredients, name_on_order)
            VALUES ('""" + ingredients_string + """', '""" + name_on_order + """')
        """

        # Show the generated SQL so user can test it (workshop style)
        #st.write(my_insert_stmt)

        # Button to trigger the insert
        time_to_insert = st.button("Submit Order")

        if time_to_insert:
            session.sql(my_insert_stmt).collect()
            st.success("Your Smoothie is ordered!", icon="✅")
