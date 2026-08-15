import streamlit as st
import pandas as pd
import math

def run():
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
