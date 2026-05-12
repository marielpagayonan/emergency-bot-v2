import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Emergency AI Assistant", page_icon="🚑")
st.title("🚑 Emergency AI Assistant")

# Sidebar for API Key
with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("Enter Gemini API Key", type="password")
    st.info("Note: Call 911 for real emergencies.")

if api_key:
    try:
        genai.configure(api_key=api_key)
        # Using the universal flash model
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        if "messages" not in st.session_state:
            st.session_state.messages = []

        for msg in st.session_state.messages:
            st.chat_message(msg["role"]).write(msg["content"])

        if prompt := st.chat_input("How can I help?"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.chat_message("user").write(prompt)
            
            response = model.generate_content(prompt)
            st.chat_message("assistant").write(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.warning("👈 Please enter your API Key in the sidebar.")
