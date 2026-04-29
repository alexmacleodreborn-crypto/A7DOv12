# app.py
import importlib.util
import os
import time
import streamlit as st
import numpy as np

try:
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

from anatomy.L01_Anatomical_Manifold import BiomechanicalBlueprint
from anatomy.L02_Muscular_System import MuscularBlueprint
from anatomy.L03_Articulations import ArticulationBlueprint
from anatomy.L04_Kinematics import KinematicEngine
from biology.L07_Growth import MaturationEngine
from core.A7DO_Brain import A7DO_Brain

# Load other modules (placeholders for now)
# You can expand these later

st.set_page_config(page_title="A7DOv12 OS - Physics Enabled", layout="wide")
st.markdown("""<style>
    .stMetric { background-color: #161b22; padding: 15px; border-radius: 12px; border: 1px solid #30363d; }
    .main { background-color: #0d1117; color: #c9d1d9; }
</style>""", unsafe_allow_html=True)

# Initialize Session State
if "a7do_brain" not in st.session_state:
    try:
        skeleton = BiomechanicalBlueprint()
        muscles = MuscularBlueprint()
        joints = ArticulationBlueprint()
        kinematics = KinematicEngine()
        growth = MaturationEngine(birth_scale=0.25)

        brain = A7DO_Brain(
            skeleton_manifold=skeleton,
            muscular_manifold=muscles,
            articulation_manifold=joints,
            kinematic_engine=kinematics,
            maturation_engine=growth,
        )

        st.session_state.a7do_brain = brain
        st.session_state.growth = growth
        print("A7DOv12 Physics System Initialized Successfully")

    except Exception as e:
        st.error(f"Initialization Error: {e}")
        st.stop()

brain = st.session_state.a7do_brain

# ====================== SIDEBAR ======================
with st.sidebar:
    st.title("🛡️ A7DOv12 OS - Physics Mode")
    st.write("### Motor Control")
    bicep_tension = st.slider("Left Bicep Tension", 0.0, 1.0, 0.0, 0.05)
    neck_tension = st.slider("Neck Flexion", 0.0, 1.0, 0.0, 0.05)
    
    st.write("### Environment")
    activity_scale = st.slider("Activity Load", 0.2, 3.0, 1.0, 0.1)
    
    # Apply controls
    brain.set_muscle_tension("BICEPS_L", bicep_tension)
    brain.set_muscle_tension("STERNOCLEIDOMASTOID_L", neck_tension)
    brain.set_muscle_tension("STERNOCLEIDOMASTOID_R", neck_tension)

# ====================== MAIN ======================
st.title("🦴 A7DOv12 - Vitruvian Physics Manifold")

col1, col2 = st.columns([3, 1])

with col1:
    if PLOTLY_AVAILABLE:
        state = brain.execute_system_pulse()
        phys = state["physics"]
        
        fig = go.Figure()
        
        # Draw Bones
        for bone_id, bone in phys["skeleton"].items():
            p = bone["proximal"]
            d = bone["distal"]
            fig.add_trace(go.Scatter3d(
                x=[p["x"], d["x"]], y=[p["z"], d["z"]], z=[p["y"], d["y"]],
                mode="lines", line=dict(color="#58a6ff", width=6), name=bone_id
            ))
        
        # Draw Muscles
        for muscle_id, muscle in phys["muscles"].items():
            o = muscle["origin"]
            i = muscle["insertion"]
            color = "#3fb950" if muscle["tension"] > 0.1 else "rgba(255,100,100,0.6)"
            width = 5 if muscle["tension"] > 0.1 else 2
            fig.add_trace(go.Scatter3d(
                x=[o["x"], i["x"]], y=[o["z"], i["z"]], z=[o["y"], i["y"]],
                mode="lines", line=dict(color=color, width=width), name=muscle_id
            ))
        
        fig.update_layout(
            margin=dict(l=0, r=0, b=0, t=30),
            scene=dict(
                xaxis=dict(visible=False),
                yaxis=dict(visible=False),
                zaxis=dict(visible=True, range=[0, 1.2]),
                aspectmode="manual",
                aspectratio=dict(x=1, y=1, z=1.8)
            ),
            title="A7DO Real-Time Physics Simulation",
            height=700
        )
        st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Physics Status")
    phys = state["physics"]
    growth = state["growth"]
    
    st.metric("Growth Stage", growth["stage"])
    st.metric("Height Scale", f"{growth['scale_x']:.3f}x")
    st.metric("Body Mass", f"{sum(b['mass'] for b in phys['skeleton'].values()):.1f} kg")
    
    stability = phys["stability"]
    delta = f"Avg: {phys['avg_stability']:.3f}"
    
    if stability > 0.75:
        st.success(f"Stability: {stability:.3f} ✓ Stable")
    elif stability > 0.5:
        st.warning(f"Stability: {stability:.3f} ⚠️ Wobbly")
    else:
        st.error(f"Stability: {stability:.3f} ☠️ Falling Risk!")
    
    st.write("**Center of Mass:**")
    st.write(f"X: {phys['com']['x']:.4f} | Z: {phys['com']['z']:.4f}")
    
    st.write("**Base of Support Area:**", phys["bos"]["area"])

# Auto refresh
time.sleep(0.3)
st.rerun()
