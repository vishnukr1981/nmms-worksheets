import streamlit as st
import random

# 1. Define the Question Bank (Expanded and Math-Formatted)
if 'questions' not in st.session_state:
    # We use r"..." (raw strings) so Python reads the math symbols correctly
    raw_questions = [
        {
            "question": "Find the missing number in the series: 2, 6, 12, 20, 30, ?",
            "options": ["36", "40", "42", "48"],
            "answer": "42",
            "explanation": "The pattern adds consecutive even numbers: +4, +6, +8, +10, +12. So, $30 + 12 = 42$."
        },
        {
            "question": r"Which number will replace the question mark? $7 \times 3 = 40$ (using a specific logical pattern). Then $5 \times 2 = ?$",
            "options": ["21", "29", "10", "15"],
            "answer": "21",
            "explanation": r"The pattern is $x^2 - y^2$. For the first one: $7^2 - 3^2 = 49 - 9 = 40$. So, $5^2 - 2^2 = 25 - 4 = 21$."
        },
        {
            "question": r"Find the missing number: 4, 9, 19, 39, ?",
            "options": ["79", "77", "75", "69"],
            "answer": "79",
            "explanation": r"The pattern is $(x \times 2) + 1$. $(39 \times 2) + 1 = 79$."
        },
        {
            "question": r"If $3x = 15$, then $x = ?$",
            "options": ["3", "4", "5", "6"],
            "answer": "5",
            "explanation": r"Divide both sides by 3. $\frac{15}{3} = 5$."
        },
        {
            "question": r"Evaluate the expression: $2^3 + 3^2$",
            "options": ["12", "17", "15", "25"],
            "answer": "17",
            "explanation": r"$2^3 = 8$ and $3^2 = 9$. Therefore, $8 + 9 = 17$."
        },
        {
            "question": r"Find the value of $x$ if $x^2 = 144$.",
            "options": ["10", "12", "14", "16"],
            "answer": "12",
            "explanation": r"The square root of 144 is 12, since $12 \times 12 = 144$."
        },
        {
            "question": "Identify the missing term: 1, 4, 9, 16, 25, ?",
            "options": ["30", "36", "40", "49"],
            "answer": "36",
            "explanation": r"These are perfect squares: $1^2, 2^2, 3^2, 4^2, 5^2$. The next is $6^2 = 36$."
        },
        {
            "question": r"Solve for $y$: $5y - 10 = 20$",
            "options": ["4", "5", "6", "8"],
            "answer": "6",
            "explanation": r"First, add 10 to both sides: $5y = 30$. Then, divide by 5: $\frac{30}{5} = 6$."
        }
    ]
    
    # Shuffle the questions so they appear in a random order every time the app loads
    random.shuffle(raw_questions)
    
    # Shuffle the multiple-choice options for each question
    for q in raw_questions:
        random.shuffle(q["options"])
        
    st.session_state.questions = raw_questions

# 2. Set up the Interface
st.title("NMMS Mental Ability Test (MAT)")
st.subheader("Arithmetic Reasoning Practice")
st.write("Test your logical and mathematical skills. Answer all the questions below and click submit to review your score.")
st.divider()

# 3. Create a form to collect all answers at once
with st.form("quiz_form"):
    student_answers = {}
    
    for i, q in enumerate(st.session_state.questions):
        st.write(f"**Question {i+1}: {q['question']}**")
        
        student_answers[i] = st.radio(
            "Select your answer:",
            q["options"],
            index=None,
            key=f"q_{i}"
        )
        st.write("---")
        
    submitted = st.form_submit_button("Submit Answers")

# 4. Grade the worksheet and show explanations
if submitted:
    score = 0
    st.header("Your Results")
    
    for i, q in enumerate(st.session_state.questions):
        student_choice = student_answers[i]
        correct_choice = q["answer"]
        
        if student_choice == correct_choice:
            score += 1
            st.success(f"Question {i+1}: Correct! ({student_choice})")
        elif student_choice == None:
            st.warning(f"Question {i+1}: You left this blank. The correct answer was {correct_choice}.")
        else:
            st.error(f"Question {i+1}: Incorrect. You chose {student_choice}. The correct answer is {correct_choice}.")
            
        # Display the explanation so the student can learn from their mistakes
        st.info(f"**Explanation:** {q['explanation']}")
        
    st.write(f"### Final Score: {score} out of {len(st.session_state.questions)}")
    
    if score == len(st.session_state.questions):
        st.balloons()