import streamlit as st
import pandas as pd

# This is the exact link to your Google Sheet database
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQIYRxNU7-vYdMaNzaAhUMUcl9c7k1LCd7fwwDw9jvBt-7Gv8qYmJrEblvQbc_1LUcB69cUAxb8F-DD/pub?output=csv"

# Fetch the data
@st.cache_data(ttl=60)
def load_data():
    return pd.read_csv(CSV_URL)

try:
    df = load_data()
except Exception as e:
    st.error("Could not load data from Google Sheets. Please check the link.")
    st.stop()

st.sidebar.title("📚 TeachNest Worksheets")

# Clean up any completely empty rows
df = df.dropna(subset=['Worksheet'])
worksheets = df['Worksheet'].unique()

if len(worksheets) == 0:
    st.warning("No worksheets found in the database. Please add some to your Google Sheet!")
    st.stop()

selected_worksheet = st.sidebar.radio("Select a Topic:", worksheets)
current_questions = df[df['Worksheet'] == selected_worksheet]

st.title(f"📝 {selected_worksheet}")
st.markdown("---")

with st.form(key=f"form_{selected_worksheet}"):
    user_answers = {}
    
    # We use enumerate(start=1) to generate a serial number (q_num) for every question
    for q_num, (index, row) in enumerate(current_questions.iterrows(), start=1):
        question_text = row['Question']
        
        # Skip if the question cell is completely empty in the spreadsheet
        if pd.isna(question_text):
            continue
            
        opt1 = str(row['Option_1'])
        opt2 = str(row['Option_2'])
        opt3 = str(row['Option_3'])
        opt4 = str(row['Option_4'])
        
        # This adds the serial number in front of the question text
        st.markdown(f"**{q_num}. {question_text}**")
        
        # Setting index=None forces the options to be blank/unselected by default
        user_answers[index] = st.radio(
            "Select answer:", 
            [opt1, opt2, opt3, opt4],
            key=f"q_{index}",
            label_visibility="collapsed",
            index=None 
        )
        st.write("") 
        
    submitted = st.form_submit_button("Submit & Review")
    
if submitted:
    score = 0
    total = 0 
    
    st.subheader("📊 Your Results")
    
    for q_num, (index, row) in enumerate(current_questions.iterrows(), start=1):
        if pd.isna(row['Question']):
            continue
            
        total += 1
        correct_ans = str(row['Correct_Answer']).strip()
        
        # Check if the user forgot to select an answer
        if user_answers[index] is None:
            st.warning(f"**Question {q_num}:** You did not select an answer. (Correct Answer: {correct_ans})")
        else:
            user_ans = str(user_answers[index]).strip()
            
            if user_ans == correct_ans:
                score += 1
                st.success(f"**Correct!** {q_num}. {row['Question']}")
            else:
                st.error(f"**Incorrect.** {q_num}. {row['Question']}")
                st.write(f"You selected: {user_ans} | **Correct Answer: {correct_ans}**")
            
        explanation = str(row['Explanation'])
        if explanation != 'nan' and explanation.strip() != '':
            st.info(f"💡 Explanation: {explanation}")
            
        st.markdown("---")
        
    st.write(f"### Final Score: {score} out of {total}")