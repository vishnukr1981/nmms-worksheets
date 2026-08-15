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

# Clean up empty rows based on Class and Worksheet
# Make sure your Google sheet has the new 'Class' column!
if 'Class' not in df.columns:
    st.error("🚨 Please add a 'Class' column to your Google Sheet!")
    st.stop()
    
df = df.dropna(subset=['Class', 'Worksheet'])

# 1. First Dropdown: Select the Class
classes = df['Class'].astype(str).unique()
selected_class = st.sidebar.selectbox("🎓 Select Your Class:", classes)

# Filter the database to only show rows for the selected class
class_df = df[df['Class'] == selected_class]

# 2. Second Dropdown: Select the Worksheet Topic
worksheets = class_df['Worksheet'].unique()

if len(worksheets) == 0:
    st.warning(f"No worksheets found for {selected_class} yet!")
    st.stop()

selected_worksheet = st.sidebar.radio("📝 Select a Topic:", worksheets)
current_questions = class_df[class_df['Worksheet'] == selected_worksheet]

st.title(f"{selected_class} - {selected_worksheet}")
st.markdown("---")

reset_key = f"reset_{selected_class}_{selected_worksheet}" 

if reset_key not in st.session_state:
    st.session_state[reset_key] = 0

score = 0
total = 0
answered_count = 0

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
    
    user_ans = st.radio(
        "Select answer:", 
        [opt1, opt2, opt3, opt4],
        key=f"q_{index}_{st.session_state[reset_key]}", 
        label_visibility="collapsed",
        index=None 
    )
    
    # INSTANT FEEDBACK LOGIC
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

st.markdown(f"## 📊 Current Score: {score} out of {total}")

if answered_count == total and total > 0:
    st.balloons()

if st.button("Restart Test"):
    st.session_state[reset_key] += 1 
    st.rerun()
