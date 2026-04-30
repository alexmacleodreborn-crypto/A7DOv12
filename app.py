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
st.title("🧬 A7DOv12 Biomechanical & Proprioceptive Monitor")

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
    st.session_state.fall_count = 0

# --- SIDEBAR CONTROLS ---
st.sidebar.header("Biological & Neural Controls")
run_sim = st.sidebar.toggle("Start Biological Clock", value=False)
speed = st.sidebar.slider("Pulse Frequency (Hz)", 1, 10, 2)

st.sidebar.divider()
st.sidebar.subheader("Neural Plasticity")
# This coefficient controls how hard the brain tries to balance
learning_rate = st.sidebar.slider("Balance Coefficient (Learning to Stand)", 0.0, 1.0, 0.1)
st.session_state.brain.balance_coefficient = learning_rate

st.sidebar.divider()
st.sidebar.subheader("Manual Override")
tension = st.sidebar.slider("Global Muscle Tension", 0.0, 1.0, 0.0)
if tension > 0:
    for mid in st.session_state.brain.muscles.registry:
        st.session_state.brain.set_muscle_tension(mid, tension)

# --- SYSTEM PULSE ---
if run_sim:
    state = st.session_state.brain.execute_system_pulse()
    st.session_state.pulse_history.append(state['physics']['stability'])
    
    # Logic for a "Fall Event"
    if state['physics']['stability'] < 0.3:
        st.session_state.fall_count += 1
        
    if len(st.session_state.pulse_history) > 50:
        st.session_state.pulse_history.pop(0)
    
    time.sleep(1/speed)
    st.rerun()
else:
    growth_stats = st.session_state.brain.growth.get_physics_state()
    # Export current static state
    state = st.session_state.brain.export_unified_state(
        growth_stats, np.zeros(3), {"area": 0.0}, 1.0, 1.0
    )

# --- MAIN LAYOUT ---
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("3D Chassis & Physics Projection")
    fig = go.Figure()

    # Draw Skeleton (Bones)[cite: 18]
    for bid, b in state['physics']['skeleton'].items():
        fig.add_trace(go.Scatter3d(
            x=[b['proximal']['x'], b['distal']['x']],
            y=[b['proximal']['y'], b['distal']['y']],
            z=[b['proximal']['z'], b['distal']['z']],
            mode='lines+markers',
            line=dict(color='silver', width=8),
            name=f"Bone: {bid}"
        ))

    # Draw Muscles (Color-coded by Neural Effort/Tension)[cite: 18]
    for mid, m in state['physics']['muscles'].items():
        t = m['tension']
        # Muscles turn red as they tighten to maintain balance
        fig.add_trace(go.Scatter3d(
            x=[m['origin']['x'], m['insertion']['x']],
            y=[m['origin']['y'], m['insertion']['y']],
            z=[m['origin']['z'], m['insertion']['z']],
            mode='lines',
            line=dict(color=f'rgb({int(255*t)}, {int(150*(1-t))}, 200)', width=4, dash='dot'),
            name=f"Muscle: {mid}"
        ))

    # Plot Center of Mass (CoM)[cite: 18]
    com = state['physics']['com']
    fig.add_trace(go.Scatter3d(
        x=[com['x']], y=[com['y']], z=[com['z']],
        mode='markers', marker=dict(color='yellow', size=10, symbol='diamond'),
        name="CoM"
    ))

    fig.update_layout(
        height=750, 
        margin=dict(l=0,r=0,b=0,t=0), 
        scene=dict(
            aspectmode='data',
            xaxis=dict(range=[-0.5, 0.5]),
            yaxis=dict(range=[0, 2.0]),
            zaxis=dict(range=[-0.5, 0.5])
        )
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Maturation & Proprioception")
    g = state['growth']
    
    # Growth Indicators[cite: 17]
    st.metric("Lifecycle Stage", g['stage'])
    st.write(f"**Physical Height Scale:** {g['scale_x']:.2%}")
    st.progress(g['scale_x'])
    
    st.divider()
    
    # Physics & Stability[cite: 18]
    p = state['physics']
    st.metric("Stability (Standing)", f"{p['stability']:.2f}", 
              delta=f"{p['stability']-p['avg_stability']:.3f}")
    
    if p['stability'] < 0.4:
        st.error("⚠️ CRITICAL INSTABILITY: Falling Risk")
    elif p['stability'] < 0.65:
        st.warning("⚖️ WOBBLING: Learning in progress")
    else:
        st.success("✅ BALANCED: Neural lock engaged")

    st.write(f"**Cumulative Falls:** {st.session_state.fall_count}")

    # Organ Development[cite: 17]
    with st.expander("Internal Organ Volumetric Scaling", expanded=True):
        for name, data in g['organs'].items():
            st.write(f"{name} Development")
            st.progress(data['capacity'])
            st.caption(f"Functional Efficiency: {data['efficiency']:.0%}")
    
    # Stability Trend
    st.subheader("Balance Calibration History")
    if st.session_state.pulse_history:
        st.line_chart(st.session_state.pulse_history)

    # Physics Metadata[cite: 18]
    st.subheader("Physics State")
    st.json({
        "Total Mass": f"{sum(b['mass'] for b in p['skeleton'].values()):.2f} kg",
        "CoM Coords": p['com'],
        "BoS Area": p['bos']['area']
    })
