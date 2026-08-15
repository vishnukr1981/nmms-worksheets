import streamlit as st
import pandas as pd
import math

st.set_page_config(page_title="Simulations", page_icon="🔬")

st.title("🔬 Interactive Simulations")
st.markdown("Explore science and math concepts by adjusting the variables below!")
st.markdown("---")

# Dropdown to select different simulations in the future
sim_choice = st.selectbox("Select a Simulation:", ["Projectile Motion"])

if sim_choice == "Projectile Motion":
    st.subheader("🚀 Projectile Motion Simulator")
    st.write("Adjust the sliders to see how velocity and angle change the path of an object!")
    
    # Create two columns for the sliders
    col1, col2 = st.columns(2)
    with col1:
        velocity = st.slider("Initial Velocity (m/s)", min_value=10, max_value=100, value=50, step=5)
    with col2:
        angle = st.slider("Launch Angle (degrees)", min_value=10, max_value=90, value=45, step=5)
        
    # Physics Calculations
    g = 9.8  # Gravity (m/s^2)
    angle_rad = math.radians(angle)
    
    # Calculate Time of Flight
    t_flight = (2 * velocity * math.sin(angle_rad)) / g
    
    # Generate data points for the graph
    t_intervals = 50
    data = []
    for i in range(t_intervals + 1):
        t = (i / t_intervals) * t_flight
        x = velocity * math.cos(angle_rad) * t
        y = (velocity * math.sin(angle_rad) * t) - (0.5 * g * t**2)
        
        if y >= 0:  # Only plot while the object is above the ground
            data.append({"Distance (m)": x, "Height (m)": y})
            
    df = pd.DataFrame(data)
    
    # Calculate Max Height and Max Range
    max_h = (velocity**2 * (math.sin(angle_rad))**2) / (2 * g)
    max_r = (velocity**2 * math.sin(2 * angle_rad)) / g
    
    # Display the results
    st.info(f"**Maximum Height:** {max_h:.2f} meters | **Total Range:** {max_r:.2f} meters")
    
    # Draw the chart
    if not df.empty:
        st.line_chart(df.set_index("Distance (m)"))
