import streamlit as st
import google.generativeai as genai
import sqlite3

# --- DATABASE LOGIC ---
def init_db():
    conn = sqlite3.connect('emergency.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS intents 
                 (keyword TEXT PRIMARY KEY, response TEXT)''')
    # Pre-loading data for your demo
    sample_data = [
        ('burn', '🔥 **DB:** Cool the burn with running water for 20 mins. Cover with cling wrap loosely.'),
        ('choking', '✋ **DB:** Perform the Heimlich maneuver: 5 back blows and 5 abdominal thrusts.'),
        ('bleeding', '🩸 **DB:** Apply firm, direct pressure to the wound using a clean cloth.')
    ]
    c.executemany('INSERT OR IGNORE INTO intents VALUES (?,?)', sample_data)
    conn.commit()
    conn.close()

def search_db(query):
    conn = sqlite3.connect('emergency.db')
    c = conn.cursor()
    c.execute("SELECT keyword, response FROM intents")
    rows = c.fetchall()
    conn.close()
    for keyword, response in rows:
        if keyword in query.lower():
            return response
    return None

# --- APP UI ---
st.set_page_config(page_title="DB Emergency Bot", page_icon="🚑")
st.title("🚑 Smart Emergency Assistant")
st.write("This bot uses a **SQLite Database** for intents and **Gemini AI** as a fallback.")

# Initialize DB
init_db()

with st.sidebar:
    st.header("Admin")
    api_key = st.text_input("Enter Gemini API Key", type="password")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("How can I help?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    
    # Check Database first
    answer = search_db(prompt)
    
    # If not in DB, try AI
    if not answer and api_key:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(prompt)
            answer = response.text
        except Exception as e:
            answer = f"AI Error: {e}. (Try asking about 'burn' or 'choking' to see the DB work!)"
    elif not answer and not api_key:
        answer = "I don't know that yet. Please provide an API key for AI help, or ask about burns/choking."

    st.chat_message("assistant").write(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})
