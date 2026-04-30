import streamlit as st
import plotly.graph_objects as go
import numpy as np
import time

# Anatomy & Biology Imports
from anatomy.L01_Anatomical_Manifold import BiomechanicalBlueprint
from anatomy.L02_Muscular_System import MuscularBlueprint
from anatomy.L03_Articulations import ArticulationBlueprint
from anatomy.L04_Kinematics import KinematicEngine
from biology.L07_Growth import MaturationEngine
from core.A7DO_Brain import A7DO_Brain

# --- DASHBOARD CONFIG ---
st.set_page_config(page_title="A7DOv12 Sentience OS", layout="wide")
st.title("🧬 A7DOv12 Biomechanical & Organic Monitor")

# Initialize Session State
if 'brain' not in st.session_state:
    st.session_state.brain = A7DO_Brain(
        BiomechanicalBlueprint(),
        MuscularBlueprint(),
        ArticulationBlueprint(),
        KinematicEngine(),
        MaturationEngine(birth_scale=0.20)
    )
    st.session_state.pulse_history = []

# --- SIDEBAR ---
st.sidebar.header("Control Panel")
run_sim = st.sidebar.toggle("Start Biological Growth", value=False)
speed = st.sidebar.slider("Pulse Frequency (Hz)", 1, 10, 2)
tension = st.sidebar.slider("Muscle Tension (Global)", 0.0, 1.0, 0.0)

# Apply global tension to all muscles
for mid in st.session_state.brain.muscles.registry:
    st.session_state.brain.set_muscle_tension(mid, tension)

# --- SYSTEM PULSE ---
if run_sim:
    state = st.session_state.brain.execute_system_pulse()
    st.session_state.pulse_history.append(state['physics']['stability'])
    if len(st.session_state.pulse_history) > 50:
        st.session_state.pulse_history.pop(0)
    time.sleep(1/speed)
    st.rerun()
else:
    # Static view if paused
    growth_stats = st.session_state.brain.growth.get_physics_state()
    state = st.session_state.brain.export_unified_state(growth_stats, np.zeros(3), {"area": 0.0}, 1.0, 1.0)

# --- LAYOUT ---
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("3D Chassis & Organic Mapping")
    fig = go.Figure()

    # Draw Skeleton (Bones)
    for bid, b in state['physics']['skeleton'].items():
        fig.add_trace(go.Scatter3d(
            x=[b['proximal']['x'], b['distal']['x']],
            y=[b['proximal']['y'], b['distal']['y']],
            z=[b['proximal']['z'], b['distal']['z']],
            mode='lines+markers',
            line=dict(color='silver', width=8),
            name=f"Bone: {bid}"
        ))

    # Draw Muscles (Color-coded by tension)
    for mid, m in state['physics']['muscles'].items():
        t = m['tension']
        fig.add_trace(go.Scatter3d(
            x=[m['origin']['x'], m['insertion']['x']],
            y=[m['origin']['y'], m['insertion']['y']],
            z=[m['origin']['z'], m['insertion']['z']],
            mode='lines',
            line=dict(color=f'rgb({int(255*t)}, {int(150*(1-t))}, 200)', width=4),
            name=f"Muscle: {mid}"
        ))

    # Center of Mass
    com = state['physics']['com']
    fig.add_trace(go.Scatter3d(
        x=[com['x']], y=[com['y']], z=[com['z']],
        mode='markers', marker=dict(color='yellow', size=8, symbol='diamond'),
        name="CoM"
    ))

    fig.update_layout(height=700, margin=dict(l=0,r=0,b=0,t=0), scene=dict(aspectmode='data'))
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Maturation Telemetry")
    g = state['growth']
    
    # Growth Indicators
    st.metric("Lifecycle Stage", g['stage'])
    st.write(f"**Height Scalar:** {g['scale_x']:.2f}")
    st.progress(g['scale_x'])
    
    st.divider()
    
    # Physics & Stability
    p = state['physics']
    st.metric("Balance Stability", f"{p['stability']:.2f}", delta=f"{p['stability']-p['avg_stability']:.3f}")
    
    if p['stability'] < 0.4:
        st.error("⚠️ HIGH FALL RISK: Chassis Unstable")
    
    # Growth-Based Organ System Scaling
    st.subheader("Organ Development")
    # Allometric scaling for internal volume
    heart_scale = g['scale_x'] ** 2.5 # Slightly faster than linear
    lung_scale = g['scale_x'] ** 3.0  # Volumetric scaling (Square-Cube)
    
    st.write("Heart Volume")
    st.progress(min(heart_scale, 1.0))
    st.write("Lung Capacity")
    st.progress(min(lung_scale, 1.0))
    
    # Stability Trend
    if st.session_state.pulse_history:
        st.line_chart(st.session_state.pulse_history)
