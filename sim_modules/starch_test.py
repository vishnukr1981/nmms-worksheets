import streamlit as st

def run():
    st.subheader("🍃 The Starch Test Virtual Lab")
    st.write("Perform the starch test on this leaf. Choose your steps carefully. If you do it in the wrong order, the experiment will fail!")
    
    if 'leaf_color' not in st.session_state:
        st.session_state.leaf_color = "Green 🟩"
        st.session_state.walls_broken = False
        st.session_state.chlorophyll_removed = False
        st.session_state.washed = False
        st.session_state.failed = False
        st.session_state.message = "You have a fresh leaf on the bench. What is your first step?"

    st.markdown("### 🔬 Lab Bench")
    
    color_map = {
        "Green 🟩": "#4CAF50",
        "Pale White ⬜": "#F5F5F5",
        "Brown/Yellow 🟫 (Failed)": "#964B00",
        "Blue-Black ⬛ (Success!)": "#000033"
    }
    
    leaf_hex = color_map.get(st.session_state.leaf_color, "#4CAF50")
    text_color = 'white' if leaf_hex in ['#4CAF50', '#000033', '#964B00'] else 'black'
    
    st.markdown(
        f"""
        <div style="background-color: {leaf_hex}; padding: 40px; border-radius: 15px; border: 3px solid #ccc; text-align: center; margin-bottom: 20px; transition: background-color 0.5s ease;">
            <h2 style="color: {text_color}; margin: 0;">Current Leaf Status: {st.session_state.leaf_color}</h2>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
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
