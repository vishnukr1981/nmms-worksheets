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

# 1. Create a unique memory key for this specific worksheet
submit_key = f"submit_{selected_worksheet}"
if submit_key not in st.session_state:
    st.session_state[submit_key] = False

# 2. This function triggers when the student hits Submit
def mark_as_submitted():
    st.session_state[submit_key] = True

score = 0
total = 0

with st.form(key=f"form_{selected_worksheet}"):
    user_answers = {}
    
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
        
        user_answers[index] = st.radio(
            "Select answer:", 
            [opt1, opt2, opt3, opt4],
            key=f"q_{index}",
            label_visibility="collapsed",
            index=None 
        )
        
        # 3. If submitted, instantly reveal the feedback right below the question
        if st.session_state[submit_key]:
            user_ans = user_answers[index]
            
            if user_ans is None:
                st.warning(f"You left this blank. **Correct Answer: {correct_ans}**")
            else:
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
        
    # 4. The button now tells the app to remember the submission
    submitted = st.form_submit_button("Submit & Review", on_click=mark_as_submitted)

# 5. Show the final score and a restart option at the bottom
if st.session_state[submit_key]:
    st.markdown(f"## 📊 Final Score: {score} out of {total}")
    
    if st.button("Restart Test"):
        st.session_state[submit_key] = False
        
        # NEW FIX: Clear the memory of every specific radio button so they deselect
        for index in current_questions.index:
            if f"q_{index}" in st.session_state:
                del st.session_state[f"q_{index}"]
                
        st.rerun()