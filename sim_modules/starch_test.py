import streamlit as st
import random

def run():
    st.header("🍃 The Starch Test")
    
    # Sub-navigation for the pedagogical phases
    phase = st.radio(
        "Select Phase:", 
        ["📖 1. Learn (Theory)", "🧪 2. Apply (Virtual Lab)", "📝 3. Review (Quiz)"], 
        horizontal=True,
        label_visibility="collapsed"
    )
    st.markdown("---")

    # ==========================================
    # PHASE 1: LEARN (THEORY)
    # ==========================================
    if phase == "📖 1. Learn (Theory)":
        st.subheader("Understanding Photosynthesis and Starch")
        st.write("""
        Plants make their own food through a process called **photosynthesis**. 
        The glucose produced during this process is converted into **starch** for storage. 
        To prove that a leaf has performed photosynthesis, we test it for the presence of starch using Iodine.
        """)
        
        st.markdown("### 🔬 The Principles of the Test")
        st.info("""
        1. **Boiling in Water:** Kills the leaf, stops all chemical reactions, and breaks down the cell walls.
        2. **Boiling in Methylated Spirit:** Extracts the green chlorophyll so we can see the final color change clearly. *(Note: Done in a water bath because spirit is highly flammable!)*
        3. **Washing in Warm Water:** Softens the brittle leaf.
        4. **Adding Iodine:** Iodine reacts with starch to produce a distinct **dark blue-black** color.
        """)
        st.success("Once you understand these steps, select **🧪 2. Apply (Virtual Lab)** at the top to conduct the experiment!")

    # ==========================================
    # PHASE 2: APPLY (VIRTUAL LAB)
    # ==========================================
    elif phase == "🧪 2. Apply (Virtual Lab)":
        st.subheader("The Virtual Lab Bench")
        st.write("Perform the starch test on this leaf. Choose your steps carefully. If you do it in the wrong order, the experiment will fail!")
        
        if 'leaf_color' not in st.session_state:
            st.session_state.leaf_color = "Green 🟩"
            st.session_state.walls_broken = False
            st.session_state.chlorophyll_removed = False
            st.session_state.washed = False
            st.session_state.failed = False
            st.session_state.message = "You have a fresh leaf on the bench. What is your first step?"

      # Map the leaf states to your actual image files
        image_map = {
            "Green 🟩": "assets/fresh_leaf.png",
            "Pale White ⬜": "assets/boiled_leaf.png",
            "Brown/Yellow 🟫 (Failed)": "assets/failed_leaf.png",
            "Blue-Black ⬛ (Success!)": "assets/success_leaf.png"
        }

        current_image_path = image_map.get(st.session_state.leaf_color)

        try:
            st.image(current_image_path, caption=f"Current Status: {st.session_state.leaf_color}", use_container_width=True)
        except Exception as e:
            st.error(f"Waiting for image upload: {current_image_path}")
        
        st.info(f"📋 **Lab Notes:** {st.session_state.message}")
        st.markdown("---")
        st.write("### 🧪 Chemical Actions")
        
        game_over = st.session_state.failed or st.session_state.leaf_color == "Blue-Black ⬛ (Success!)"
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("💧 Boil in Water", disabled=game_over, use_container_width=True):
                if not st.session_state.walls_broken:
                    st.session_state.walls_broken = True
                    st.session_state.message = "Good! The boiling water killed the leaf and broke down the cell walls."
                else:
                    st.session_state.message = "You already boiled it in water! Move on to the next step."
                st.rerun()
                
        with col2:
            if st.button("🔥 Boil in Spirit", disabled=game_over, use_container_width=True):
                if st.session_state.walls_broken and not st.session_state.chlorophyll_removed:
                    st.session_state.chlorophyll_removed = True
                    st.session_state.leaf_color = "Pale White ⬜"
                    st.session_state.message = "Excellent. The methylated spirit extracted the green chlorophyll. The leaf is now pale and very brittle."
                elif not st.session_state.walls_broken:
                    st.session_state.failed = True
                    st.session_state.message = "❌ ERROR: You must break down the cell walls first by boiling in water! The spirit couldn't penetrate properly."
                else:
                    st.session_state.message = "The chlorophyll is already removed."
                st.rerun()
                
        with col3:
            if st.button("🚰 Wash in Warm Water", disabled=game_over, use_container_width=True):
                if st.session_state.chlorophyll_removed and not st.session_state.washed:
                    st.session_state.washed = True
                    st.session_state.message = "Perfect. You washed off the spirit and softened the brittle leaf so it can absorb the iodine."
                elif not st.session_state.chlorophyll_removed:
                    st.session_state.message = "Rinsing a fresh/boiled leaf doesn't do anything right now. Extract the chlorophyll first."
                else:
                    st.session_state.message = "Leaf is already washed and softened."
                st.rerun()
                
        with col4:
            if st.button("🩸 Add Iodine", disabled=game_over, use_container_width=True):
                if st.session_state.washed and st.session_state.chlorophyll_removed:
                    st.session_state.leaf_color = "Blue-Black ⬛ (Success!)"
                    st.session_state.message = "🎉 SUCCESS! The iodine reacted with the starch. You completed the experiment perfectly!"
                elif st.session_state.chlorophyll_removed and not st.session_state.washed:
                    st.session_state.failed = True
                    st.session_state.leaf_color = "Brown/Yellow 🟫 (Failed)"
                    st.session_state.message = "❌ ERROR: The leaf was too brittle and full of spirit! You forgot to rinse and soften it first. The iodine rolled right off."
                elif not st.session_state.chlorophyll_removed:
                    st.session_state.failed = True
                    st.session_state.leaf_color = "Brown/Yellow 🟫 (Failed)"
                    st.session_state.message = "❌ ERROR: The green chlorophyll masked the color change, and the cuticle blocked the iodine! Experiment failed."
                st.rerun()

        if game_over:
            st.markdown("---")
            if st.button("🔄 Clean the Lab Bench & Restart", use_container_width=True):
                st.session_state.leaf_color = "Green 🟩"
                st.session_state.walls_broken = False
                st.session_state.chlorophyll_removed = False
                st.session_state.washed = False
                st.session_state.failed = False
                st.session_state.message = "You have a fresh leaf on the bench. What is your first step?"
                st.rerun()
                
        if st.session_state.leaf_color == "Blue-Black ⬛ (Success!)":
            st.balloons()
            st.success("Great job! Now click **📝 3. Review (Quiz)** at the top to test your knowledge.")

    # ==========================================
    # PHASE 3: REVIEW (QUIZ)
    # ==========================================
    elif phase == "📝 3. Review (Quiz)":
        st.subheader("Laboratory Review Quiz")
        st.write("Test your understanding of the chemical reactions you just performed!")
        
        # Initialize quiz state
        if 'starch_quiz_score' not in st.session_state:
            st.session_state.starch_quiz_submitted = False
            st.session_state.starch_quiz_score = 0
            
        # Hardcoded randomized structure for the anchor module
        q1_opts = ["To extract chlorophyll", "To break down cell walls", "To add starch", "To soften the leaf"]
        q2_opts = ["Water", "Iodine", "Methylated Spirit", "Hydrochloric Acid"]
        q3_opts = ["Brown", "Pale White", "Blue-Black", "Red"]
        
        # We use a quick trick to keep options stable per session but functionally shuffled
        if 'q1_shuffled' not in st.session_state:
            st.session_state.q1_shuffled = random.sample(q1_opts, len(q1_opts))
            st.session_state.q2_shuffled = random.sample(q2_opts, len(q2_opts))
            st.session_state.q3_shuffled = random.sample(q3_opts, len(q3_opts))

        with st.form("starch_quiz"):
            st.markdown("**1. Why do we boil the leaf in water during the first step?**")
            ans1 = st.radio("Q1", st.session_state.q1_shuffled, label_visibility="collapsed", index=None)
            
            st.markdown("**2. Which chemical is used to extract the green chlorophyll?**")
            ans2 = st.radio("Q2", st.session_state.q2_shuffled, label_visibility="collapsed", index=None)
            
            st.markdown("**3. What color indicates a positive presence of starch?**")
            ans3 = st.radio("Q3", st.session_state.q3_shuffled, label_visibility="collapsed", index=None)
            
            submit = st.form_submit_button("Submit Answers")
            
            if submit:
                score = 0
                st.session_state.starch_quiz_submitted = True
                
                st.markdown("---")
                if ans1 == "To break down cell walls":
                    score += 1
                    st.success("✅ Q1 Correct: Boiling water breaks down cell walls and stops reactions.")
                else:
                    st.error(f"❌ Q1 Incorrect: You chose '{ans1}'. The correct answer is 'To break down cell walls'.")
                    
                if ans2 == "Methylated Spirit":
                    score += 1
                    st.success("✅ Q2 Correct: Methylated spirit dissolves and removes the chlorophyll.")
                else:
                    st.error(f"❌ Q2 Incorrect: You chose '{ans2}'. The correct answer is 'Methylated Spirit'.")
                    
                if ans3 == "Blue-Black":
                    score += 1
                    st.success("✅ Q3 Correct: Iodine turns blue-black in the presence of starch.")
                else:
                    st.error(f"❌ Q3 Incorrect: You chose '{ans3}'. The correct answer is 'Blue-Black'.")
                    
                st.session_state.starch_quiz_score = score
                
        if st.session_state.starch_quiz_submitted:
            st.info(f"### 📊 Final Score: {st.session_state.starch_quiz_score} / 3")
            if st.session_state.starch_quiz_score == 3:
                st.balloons()
            
            if st.button("Retake Quiz"):
                st.session_state.starch_quiz_submitted = False
                st.session_state.starch_quiz_score = 0
                st.session_state.q1_shuffled = random.sample(q1_opts, len(q1_opts))
                st.session_state.q2_shuffled = random.sample(q2_opts, len(q2_opts))
                st.session_state.q3_shuffled = random.sample(q3_opts, len(q3_opts))
                st.rerun()
