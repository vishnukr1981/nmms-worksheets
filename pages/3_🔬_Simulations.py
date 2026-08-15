import streamlit as st
import pandas as pd
import math

st.set_page_config(page_title="Simulations", page_icon="🔬", layout="wide")

st.title("🔬 Interactive Simulations")
st.markdown("Explore science and math concepts by adjusting the variables below!")
st.markdown("---")

sim_choice = st.selectbox("Select a Simulation:", ["Projectile Motion", "Starch Test (Biology)"])

if sim_choice == "Projectile Motion":
    st.subheader("🚀 Projectile Motion Simulator")
    st.write("Adjust the sliders to see how velocity and angle change the path of an object!")
    
    col1, col2 = st.columns(2)
    with col1:
        velocity = st.slider("Initial Velocity (m/s)", min_value=10, max_value=100, value=50, step=5)
    with col2:
        angle = st.slider("Launch Angle (degrees)", min_value=10, max_value=90, value=45, step=5)
        
    g = 9.8  
    angle_rad = math.radians(angle)
    t_flight = (2 * velocity * math.sin(angle_rad)) / g
    
    t_intervals = 50
    data = []
    for i in range(t_intervals + 1):
        t = (i / t_intervals) * t_flight
        x = velocity * math.cos(angle_rad) * t
        y = (velocity * math.sin(angle_rad) * t) - (0.5 * g * t**2)
        if y >= 0:  
            data.append({"Distance (m)": x, "Height (m)": y})
            
    df = pd.DataFrame(data)
    max_h = (velocity**2 * (math.sin(angle_rad))**2) / (2 * g)
    max_r = (velocity**2 * math.sin(2 * angle_rad)) / g
    
    st.info(f"**Maximum Height:** {max_h:.2f} meters | **Total Range:** {max_r:.2f} meters")
    if not df.empty:
        st.line_chart(df.set_index("Distance (m)"))

# --- UPGRADED STARCH TEST SIMULATION ---
elif sim_choice == "Starch Test (Biology)":
    st.subheader("🍃 The Starch Test Virtual Lab")
    st.write("Perform the starch test on this leaf. Choose your steps carefully. If you do it in the wrong order, the experiment will fail!")
    
    # Initialize the leaf's physical states in memory
    if 'leaf_color' not in st.session_state:
        st.session_state.leaf_color = "Green 🟩"
        st.session_state.walls_broken = False
        st.session_state.chlorophyll_removed = False
        st.session_state.washed = False
        st.session_state.failed = False
        st.session_state.message = "You have a fresh leaf on the bench. What is your first step?"

    # --- VISUAL DISPLAY OF THE LEAF ---
    st.markdown("### 🔬 Lab Bench")
    
    color_map = {
        "Green 🟩": "#4CAF50",
        "Pale White ⬜": "#F5F5F5",
        "Brown/Yellow 🟫 (Failed)": "#964B00",
        "Blue-Black ⬛ (Success!)": "#000033"
    }
    
    leaf_hex = color_map.get(st.session_state.leaf_color, "#4CAF50")
    text_color = 'white' if leaf_hex in ['#4CAF50', '#000033', '#964B00'] else 'black'
    
    # Draw the dynamic leaf visual
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
    
    # Disable buttons if the student fails or succeeds
    game_over = st.session_state.failed or st.session_state.leaf_color == "Blue-Black ⬛ (Success!)"

    # Display all chemicals at once (Decoys included)
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
