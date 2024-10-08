# -*- coding: utf-8 -*-
"""foodrecommend.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1SGeKEzRNyObt02SVJR-uJ6bZ4VUyUVBs
"""

import os
import pandas as pd
import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.pydantic_v1 import BaseModel, Field
import subprocess

# Set up the Streamlit page
st.set_page_config(page_title="Food Suggestion System", page_icon="🍴", layout="wide")

# Define the title and description
st.title("🍴 Food Suggestion System")
st.markdown("""
    Welcome to the Food Suggestion System! 🌟
    Enter your mood, current weather, and preference (veg or non-veg) below, and we'll recommend some delicious food for you.
    Just fill out the fields and click 'Get Suggestion' to receive personalized recommendations!
""")

# Get the API key from environment variables
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "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")

# Initialize the language model if API key is available
if not GROQ_API_KEY:
    st.error("API key is not set. Please configure the API key in the environment variables.")
else:
    try:
        # Initialize the language model with the API key
        llm = ChatGroq(model="llama-3.1-70b-versatile", api_key=GROQ_API_KEY)
    except Exception as e:
        st.error(f"Failed to initialize the language model: {e}")

    # Define the Pydantic classes
    class FoodSuggestion(BaseModel):
        Food_Recommendation: str = Field(description="Suggested food based on mood, weather, and preference")

    class Response(BaseModel):
        output: FoodSuggestion

    # Function to display the response
    def display_food_suggestion(response: Response):
        if isinstance(response.output, FoodSuggestion):
            suggestion = response.output.Food_Recommendation
            st.write(f"### Food Recommendation: {suggestion}")
        else:
            st.error("Unknown response type received.")

    # Structure the model to return output based on the schema
    try:
        structured_llm = llm.with_structured_output(Response)
    except Exception as e:
        st.error(f"Error in structuring the language model output: {e}")

    # Create input form
    with st.form(key='input_form'):
        st.header("Please Enter Your Details")
        mood = st.text_input("Your Mood", placeholder="e.g., happy, sad, excited")
        weather = st.text_input("Current Weather", placeholder="e.g., sunny, cloudy, rainy")
        preference = st.selectbox("Food Preference", ["non-veg", "veg"])
        submit_button = st.form_submit_button(label="Get Suggestion")

    # Submit button action
    if submit_button:
        if not mood or not weather:
            st.error("Please enter both mood and weather before submitting.")
        else:
            try:
                # Construct the input query
                input_text = (f"Suggest {preference} food for a person who is feeling {mood} "
                              f"and the weather is {weather}.")

                # Invoke the model and display the result
                response = structured_llm.invoke(input_text)
                display_food_suggestion(response)
            except Exception as e:
                if 'tool_use_failed' in str(e):
                    st.error("Please try to submit again. Ensure your input is clear and valid.")
                else:
                    st.error(f"Unable to process the query: {e}")
