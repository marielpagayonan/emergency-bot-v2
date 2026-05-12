import streamlit as st
import google.generativeai as genai

# 1. Page Configuration
st.set_page_config(page_title="Emergency AI Assistant", page_icon="🚑", layout="centered")

# 2. Styling
st.title("🚑 Smart Emergency Assistant")
st.markdown("---")

# 3. Sidebar Setup
with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("Enter Gemini API Key", type="password")
    
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()
        
    st.divider()
    st.warning("**DISCLAIMER:** This is an AI tool for educational purposes. In a real life-threatening emergency, always call **911** or your local emergency number immediately.")

# 4. Logic & AI Configuration
if api_key:
    try:
        genai.configure(api_key=api_key)
        # Using 1.5-flash which is the most stable for free tier
        model = genai.GenerativeModel('gemini-1.5-flash')

        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Display chat history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Chat Input
        if prompt := st.chat_input("Describe the emergency (e.g., 'What to do for a burn?')"):
            # Add user message to history
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # Generate and display assistant response
            with st.chat_message("assistant"):
                # Instructions to keep AI focused and brief (saves your quota!)
                system_instruction = f"Provide brief, calm, step-by-step first aid advice for: {prompt}. Be concise."
                
                try:
                    response = model.generate_content(system_instruction)
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                except Exception as e:
                    if "429" in str(e):
                        st.error("Quota full! Please wait 60 seconds before typing again.")
                    else:
                        st.error(f"AI Error: {e}")

    except Exception as e:
        st.error(f"Configuration Error: {e}")
else:
    st.info("👈 Please enter your Gemini API Key in the sidebar to start the assistant.")
    st.image("https://img.icons8.com/clouds/200/medical-doctor.png") # Adds a nice visual touch
