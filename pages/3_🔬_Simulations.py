
import streamlit as st
from sim_modules import projectile_motion, starch_test

st.set_page_config(page_title="Simulations", page_icon="🔬", layout="wide")

st.title("🔬 Interactive Laboratory")
st.markdown("Select a scientific department below to explore our interactive experiments!")
st.markdown("---")

# Create the subject tabs
tab_bio, tab_chem, tab_phys, tab_math = st.tabs(["🧬 Biology", "🧪 Chemistry", "🔭 Physics", "📐 Mathematics"])

# --- BIOLOGY DEPARTMENT ---
with tab_bio:
    st.subheader("🧬 Biology Laboratory")
    bio_choice = st.selectbox("Select an experiment:", ["Starch Test (Leaf)"], key="bio_select")
    st.markdown("---")
    
    if bio_choice == "Starch Test (Leaf)":
        starch_test.run()

# --- CHEMISTRY DEPARTMENT ---
with tab_chem:
    st.subheader("🧪 Chemistry Laboratory")
    st.info("New chemistry experiments (like Acid/Base testing) are being set up! Check back soon.")

# --- PHYSICS DEPARTMENT ---
with tab_phys:
    st.subheader("🔭 Physics Laboratory")
    phys_choice = st.selectbox("Select an experiment:", ["Projectile Motion"], key="phys_select")
    st.markdown("---")
    
    if phys_choice == "Projectile Motion":
        projectile_motion.run()

# --- MATHEMATICS DEPARTMENT ---
with tab_math:
    st.subheader("📐 Mathematics Laboratory")
    st.info("Interactive math and geometry tools are coming soon!")
