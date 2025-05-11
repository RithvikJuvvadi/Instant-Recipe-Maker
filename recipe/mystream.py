import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

genai.configure(api_key="AIzaSyANn8ZhKPr6UYnqlwBzghedR022_30yT1Y")

# Initialize the Gemini model
model = genai.GenerativeModel("gemini-2.0-flash")
# Function to get response from Gemini
def get_gemini_response(question):
    response = model.generate_content(question)
    return response

# Streamlit page setup
st.set_page_config(page_title="Recipe Generator AI", layout="wide")

# Optional CSS loader
def local_css(file_name):
    css_path = os.path.join(os.path.dirname(__file__), file_name)
    try:
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("Custom CSS file not found. Styling skipped.")

# Load styles if available
local_css("styles1.css")

st.header("Recipe Generator AI")

# Initialize session history
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# User input area
user_input = st.text_area("Enter the ingredients you have:", key="input")

# Generate button
if st.button("Generate Recipe") and user_input:
    prompt = f"Generate a recipe using the following ingredients: {user_input}"
    try:
        response = get_gemini_response(prompt)
        response_text = response.text

        # Store history
        st.session_state["chat_history"].append(("You", user_input))
        st.session_state["chat_history"].append(("Bot", response_text))

        # Display output
        st.subheader("Generated Recipe:")
        st.markdown(f'<div class="response">{response_text}</div>', unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error generating response: {e}")

# Display chat history
st.subheader("Chat History")
for role, message in st.session_state["chat_history"]:
    if role == "Bot":
        st.markdown(f"**{role}:** {message}")
    else:
        st.write(f"{role}: {message}")
