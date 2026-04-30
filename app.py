import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import time

# Importing your modules (ensure your folder structure allows these imports)
from anatomy.L01_Anatomical_Manifold import BiomechanicalBlueprint
from anatomy.L02_Muscular_System import MuscularBlueprint
from anatomy.L03_Articulations import ArticulationBlueprint
from anatomy.L04_Kinematics import KinematicEngine
from biology.L07_Growth import MaturationEngine
from core.A7DO_Brain import A7DO_Brain

# --- DASHBOARD CONFIG ---
st.set_page_config(page_title="A7DOv12 Sentience OS Monitor", layout="wide")
st.title("🧬 A7DOv12 Biomechanical Dashboard")

# Initialize State in Streamlit Session
if 'brain' not in st.session_state:
    st.session_state.brain = A7DO_Brain(
        BiomechanicalBlueprint(),
        MuscularBlueprint(),
        ArticulationBlueprint(),
        KinematicEngine(),
        MaturationEngine()
    )
    st.session_state.pulse_history = []

# --- SIDEBAR CONTROLS ---
st.sidebar.header("System Controls")
run_sim = st.sidebar.toggle("Pulse System (Live)", value=False)
speed = st.sidebar.slider("Sim Speed (Hz)", 1, 10, 2)
tension_slider = st.sidebar.slider("Global Muscle Tension", 0.0, 1.0, 0.0)

# Apply manual tension to all muscles for testing
for mid in st.session_state.brain.muscles.registry:
    st.session_state.brain.set_muscle_tension(mid, tension_slider)

# --- SYSTEM PULSE ---
if run_sim:
    state = st.session_state.brain.execute_system_pulse()
    st.session_state.pulse_history.append(state['physics']['stability'])
    if len(st.session_state.pulse_history) > 50:
        st.session_state.pulse_history.pop(0)
    time.sleep(1/speed)
    st.rerun()
else:
    # Get current state without advancing growth if paused
    growth_stats = st.session_state.brain.growth.get_physics_state()
    st.session_state.brain.skeleton.generate_current_geometry(growth_stats["scale_x"])
    st.session_state.brain.muscles.generate_current_musculature(st.session_state.brain.skeleton.registry)
    # Dummy stability for initial load
    state = st.session_state.brain.export_unified_state(growth_stats, [0,0,0], {"area":0}, 1.0, 1.0)

# --- UI LAYOUT ---
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("3D Anatomical View")
    
    fig = go.Figure()

    # 1. Plot Bones (Skeleton)
    for bid, b_data in state['physics']['skeleton'].items():
        prox = b_data['proximal']
        dist = b_data['distal']
        fig.add_trace(go.Scatter3d(
            x=[prox['x'], dist['x']], y=[prox['y'], dist['y']], z=[prox['z'], dist['z']],
            mode='lines+markers',
            line=dict(color='lightgray', width=8),
            name=f"Bone: {bid}",
            hoverinfo='text',
            text=f"{bid} | Mass: {b_data['mass']:.2f}kg"
        ))

    # 2. Plot Muscles
    for mid, m_data in state['physics']['muscles'].items():
        # Change color based on tension
        t_val = m_data['tension']
        m_color = f'rgb({int(255*t_val)}, {int(100*(1-t_val))}, 100)'
        
        fig.add_trace(go.Scatter3d(
            x=[m_data['origin']['x'], m_data['insertion']['x']],
            y=[m_data['origin']['y'], m_data['insertion']['y']],
            z=[m_data['origin']['z'], m_data['insertion']['z']],
            mode='lines',
            line=dict(color=m_color, width=4, dash='dot'),
            name=f"Muscle: {mid}"
        ))

    # 3. Plot Center of Mass (CoM)
    com = state['physics']['com']
    fig.add_trace(go.Scatter3d(
        x=[com['x']], y=[com['y']], z=[com['z']],
        mode='markers',
        marker=dict(color='yellow', size=10, symbol='diamond'),
        name="Center of Mass"
    ))

    fig.update_layout(
        scene=dict(aspectmode='data', xaxis_title="X", yaxis_title="Y", zaxis_title="Z"),
        margin=dict(l=0, r=0, b=0, t=0),
        height=700
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Biometric Telemetry")
    
    # Growth Metrics
    g = state['growth']
    st.metric("Maturation Stage", g['stage'])
    st.progress(g['scale_x'], text=f"Height Scale: {g['scale_x']:.2f}")
    
    # Physics Metrics
    p = state['physics']
    st.metric("Stability Score", f"{p['stability']:.2f}", 
              delta=f"{p['stability'] - p['avg_stability']:.3f}")
    
    if p['stability'] < 0.4:
        st.error("⚠️ CRITICAL UNSTABLE STATE")
    elif p['stability'] < 0.65:
        st.warning("⚖️ BALANCE CHALLENGED")
    else:
        st.success("✅ STABLE STANCE")

    # Stability Trend
    if st.session_state.pulse_history:
        st.line_chart(st.session_state.pulse_history)

    # Technical Details
    with st.expander("System Internals"):
        st.json({
            "Mass (Total)": f"{sum(b['mass'] for b in state['physics']['skeleton'].values()):.2f} kg",
            "BoS Area": p['bos']['area'],
            "Growth Factors": g
        })
