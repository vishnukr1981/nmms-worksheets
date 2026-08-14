import streamlit as st
import pandas as pd

# Your exact Google Sheet database link
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQIYRxNU7-vYdMaNzaAhUMUcl9c7k1LCd7fwwDw9jvBt-7Gv8qYmJrEblvQbc_1LUcB69cUAxb8F-DD/pub?output=csv"

@st.cache_data(ttl=60)
def load_data():
    return pd.read_csv(CSV_URL)

try:
    df = load_data()
except Exception as e:
    st.error("Could not load data from Google Sheets. Please check the link.")
    st.stop()

st.sidebar.title("📚 TeachNest Worksheets")

# Clean up empty rows and get worksheets
df = df.dropna(subset=['Worksheet'])
worksheets = df['Worksheet'].unique()

if len(worksheets) == 0:
    st.warning("No worksheets found in the database. Please add some to your Google Sheet!")
    st.stop()

selected_worksheet = st.sidebar.radio("Select a Topic:", worksheets)
current_questions = df[df['Worksheet'] == selected_worksheet]

st.title(f"📝 {selected_worksheet}")
st.markdown("---")

# We only need the reset key now. No submit key needed since it is instant!
reset_key = f"reset_{selected_worksheet}" 

if reset_key not in st.session_state:
    st.session_state[reset_key] = 0

score = 0
total = 0
answered_count = 0

# Notice there is no 'with st.form():' anymore. 
# Every click instantly triggers the logic below!

for q_num, (index, row) in enumerate(current_questions.iterrows(), start=1):
    question_text = row['Question']
    
    if pd.isna(question_text):
        continue
        
    total += 1
    opt1 = str(row['Option_1'])
    opt2 = str(row['Option_2'])
    opt3 = str(row['Option_3'])
    opt4 = str(row['Option_4'])
    correct_ans = str(row['Correct_Answer']).strip()
    
    st.markdown(f"**{q_num}. {question_text}**")
    
    # The radio button will trigger an instant update when clicked
    user_ans = st.radio(
        "Select answer:", 
        [opt1, opt2, opt3, opt4],
        key=f"q_{index}_{st.session_state[reset_key]}", 
        label_visibility="collapsed",
        index=None 
    )
    
    # INSTANT FEEDBACK LOGIC
    # If user_ans is not None, it means the student just clicked an option
    if user_ans is not None:
        answered_count += 1
        user_ans = str(user_ans).strip()
        
        if user_ans == correct_ans:
            score += 1
            st.success("**Correct!**")
        else:
            st.error(f"**Incorrect.** You selected: {user_ans} | **Correct Answer: {correct_ans}**")
        
        explanation = str(row['Explanation'])
        if explanation != 'nan' and explanation.strip() != '':
            st.info(f"💡 Explanation: {explanation}")
            
    st.write("---") 

# Show score dynamically at the bottom
st.markdown(f"## 📊 Current Score: {score} out of {total}")

# Trigger a fun animation if they finish the whole worksheet
if answered_count == total and total > 0:
    st.balloons()

# Restart button increments the counter to wipe all radio buttons blank
if st.button("Restart Test"):
    st.session_state[reset_key] += 1 
    st.rerun()