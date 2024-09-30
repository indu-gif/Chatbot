import os
import streamlit as st
import openai

# Set API key directly for testing (optional)
# openai.api_key = "your_api_key_here"  # Uncomment for testing

# Load API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

# Set Streamlit page configuration - this must be the first Streamlit command
st.set_page_config(page_title="GPT-4o Chat", page_icon="🗪", layout="centered")

# Check if the API key is loaded correctly
if openai.api_key is None:
    st.error("API key is not set. Please set the OPENAI_API_KEY environment variable.")
else:
    st.success("API key loaded successfully!")

# Initialize chat session
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Streamlit page title
st.title("👀 GPT-4o - ChatBot")

# Display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input field for user's message
user_prompt = st.chat_input("Find your next adventure....")

if user_prompt:
    st.chat_message("user").markdown(user_prompt)
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})

    try:
        # Send user's message to GPT-4o
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "You are a helpful assistant"}, *st.session_state.chat_history]
        )
        assistant_response = response.choices[0].message["content"]
    except Exception as e:
        assistant_response = f"An error occurred: {str(e)}"

    st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})

    # Display GPT-4o's response
    with st.chat_message("assistant"):
        st.markdown(assistant_response)

# Clear chat button
if st.button("Clear Chat"):
    st.session_state.chat_history = []
