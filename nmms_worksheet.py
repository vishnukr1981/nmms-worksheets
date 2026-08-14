import streamlit as st
import pandas as pd

# This is the exact link to your Google Sheet database
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQIYRxNU7-vYdMaNzaAhUMUcl9c7k1LCd7fwwDw9jvBt-7Gv8qYmJrEblvQbc_1LUcB69cUAxb8F-DD/pub?output=csv"

# Fetch the data (the ttl=60 tells Streamlit to check for updates every 60 seconds)
@st.cache_data(ttl=60)
def load_data():
    return pd.read_csv(CSV_URL)

# Attempt to load the database
try:
    df = load_data()
except Exception as e:
    st.error("Could not load data from Google Sheets. Please check the link.")
    st.stop()

# Set up the Sidebar
st.sidebar.title("📚 TeachNest Worksheets")

# Get a list of all unique worksheet names from Column A
worksheets = df['Worksheet'].dropna().unique()

if len(worksheets) == 0:
    st.warning("No worksheets found in the database. Please add some to your Google Sheet!")
    st.stop()

# Create the menu automatically based on the Google Sheet
selected_worksheet = st.sidebar.radio("Select a Topic:", worksheets)

# Filter the data so it ONLY shows questions for the selected worksheet
current_questions = df[df['Worksheet'] == selected_worksheet]

st.title(f"📝 {selected_worksheet}")
st.markdown("---")

# Build the interactive form dynamically
with st.form(key=f"form_{selected_worksheet}"):
    user_answers = {}
    
    # Loop through every row in the spreadsheet for this worksheet
    for index, row in current_questions.iterrows():
        question_text = row['Question']
        opt1 = str(row['Option_1'])
        opt2 = str(row['Option_2'])
        opt3 = str(row['Option_3'])
        opt4 = str(row['Option_4'])
        
        st.markdown(f"**{question_text}**")
        
        user_answers[index] = st.radio(
            "Select answer:", 
            [opt1, opt2, opt3, opt4],
            key=f"q_{index}",
            label_visibility="collapsed"
        )
        st.write("") 
        
    # The big submit button at the bottom
    submitted = st.form_submit_button("Submit & Review")
    
# Grading Logic
if submitted:
    score = 0
    total = len(current_questions)
    
    st.subheader("📊 Your Results")
    
    for index, row in current_questions.iterrows():
        # Clean up the text just in case there are invisible spaces in the spreadsheet
        correct_ans = str(row['Correct_Answer']).strip()
        user_ans = str(user_answers[index]).strip()
        
        if user_ans == correct_ans:
            score += 1
            st.success(f"**Correct!** {row['Question']}")
        else:
            st.error(f"**Incorrect.** {row['Question']}")
            st.write(f"You selected: {user_ans} | **Correct Answer: {correct_ans}**")
            
        # Show explanation if one exists in Column H
        explanation = str(row['Explanation'])
        if explanation != 'nan' and explanation.strip() != '':
            st.info(f"💡 Explanation: {explanation}")
            
        st.markdown("---")
        
    st.write(f"### Final Score: {score} out of {total}")