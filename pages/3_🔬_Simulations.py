import streamlit as st
from sim_modules import projectile_motion, starch_test

st.set_page_config(page_title="Simulations", page_icon="🔬", layout="wide")

st.title("🔬 Interactive Simulations")
st.markdown("Explore science and math concepts by adjusting the variables below!")
st.markdown("---")

# The Dropdown Menu
sim_choice = st.selectbox("Select a Simulation:", ["Projectile Motion", "Starch Test (Biology)"])

# The Modular Router
if sim_choice == "Projectile Motion":
    projectile_motion.run()
    
elif sim_choice == "Starch Test (Biology)":
    starch_test.run()
