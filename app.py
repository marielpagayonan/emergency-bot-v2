import streamlit as st
import google.generativeai as genai
# Setup ng hitsura ng website
st.set_page_config(page_title="Emergency AI Assistant", page_icon="🚑")

st.title("🚑 Smart Emergency Assistant")
st.write("Welcome! This AI provides safety guidance for emergencies.")

# Sidebar para sa API Key
with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("Enter Gemini API Key", type="password")
    st.warning("Note: Always call 911 for immediate life-threatening emergencies.")

if api_key:
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')

        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Display chat history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Chat Input
        if prompt := st.chat_input("How can I help you?"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                # Tinuturuan ang AI na maging emergency expert
                emergency_context = f"You are an emergency first-aid expert. Give clear, calm, and short advice for: {prompt}. Remind them to call 911 if it sounds dangerous."
                response = model.generate_content(emergency_context)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"May error sa API Key mo: {e}")
else:
    st.info("👈 Pakilagay ang API Key mo sa sidebar para magising ang bot.")
