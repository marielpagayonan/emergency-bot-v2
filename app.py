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
        # Configure Gemini
        genai.configure(api_key=api_key)

        # Updated working model
        model = genai.GenerativeModel("gemini-2.0-flash")

        # Chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Display previous messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # User input
        if prompt := st.chat_input("How can I help you?"):

            # Save user message
            st.session_state.messages.append({
                "role": "user",
                "content": prompt
            })

            with st.chat_message("user"):
                st.markdown(prompt)

            # Generate AI response
            with st.chat_message("assistant"):

                response = model.generate_content(prompt)

                reply = response.text

                st.markdown(reply)

                # Save assistant reply
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": reply
                })

    except Exception as e:
        st.error(f"Error: {e}")

else:
    st.info("👈 Please enter your API Key in the sidebar.")
