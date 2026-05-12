import streamlit as st
import google.generativeai as genai

# Setup
st.set_page_config(page_title="Emergency AI Assistant", page_icon="🚑")
st.title("🚑 Smart Emergency Assistant")
st.write("Welcome! This AI provides safety guidance for emergencies.")

# Sidebar
with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("Enter Gemini API Key", type="password")
    st.warning("Note: Always call 911 for immediate life-threatening emergencies.")

if api_key:
    try:
        genai.configure(api_key=api_key)
        # Using the most stable model name for version 1.5
        model = genai.GenerativeModel('gemini-1.5-flash')

        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("How can I help you?"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.info("👈 Please enter your API Key in the sidebar.")
