import streamlit as st
import pandas as pd
import math

st.set_page_config(page_title="Simulations", page_icon="🔬")

st.title("🔬 Interactive Simulations")
st.markdown("Explore science and math concepts by adjusting the variables below!")
st.markdown("---")

# Dropdown to select different simulations
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

# --- NEW STARCH TEST EXPERIMENT ---
elif sim_choice == "Starch Test (Biology)":
    st.subheader("🍃 The Starch Test Procedure")
    st.write("Follow the correct laboratory sequence to test this leaf for starch!")
    
    # Initialize session state to remember the student's progress
    if 'starch_stage' not in st.session_state:
        st.session_state.starch_stage = 0
        
    # Stage 0: Fresh Leaf
    if st.session_state.starch_stage == 0:
        st.info("🧪 **Current Status:** You have a fresh, green leaf freshly picked from the sunlight.")
        if st.button("💧 Boil in Water (1-2 mins)"):
            st.session_state.starch_stage = 1
            st.rerun()
            
    # Stage 1: Boiled in Water
    elif st.session_state.starch_stage == 1:
        st.info("🧪 **Current Status:** The leaf is boiled. Cell walls are broken down.")
        if st.button("🔥 Boil in Methylated Spirit (Water Bath)"):
            st.session_state.starch_stage = 2
            st.rerun()
            
    # Stage 2: Boiled in Spirit
    elif st.session_state.starch_stage == 2:
        st.info("🧪 **Current Status:** The chlorophyll is extracted. The leaf is now pale white and very brittle.")
        if st.button("🚰 Rinse in Warm Water"):
            st.session_state.starch_stage = 3
            st.rerun()
            
    # Stage 3: Rinsed
    elif st.session_state.starch_stage == 3:
        st.info("🧪 **Current Status:** The leaf is softened and spread out flat on a white tile.")
        if st.button("🩸 Add Iodine Solution"):
            st.session_state.starch_stage = 4
            st.rerun()
            
    # Stage 4: Result
    elif st.session_state.starch_stage == 4:
        st.success("🎉 **Result:** The leaf turned dark BLUE-BLACK! Starch is definitely present.")
        st.balloons()
        if st.button("🔄 Restart Experiment"):
            st.session_state.starch_stage = 0
            st.rerun()
