
# A7DOv12 Sentience OS
# File 5: app.py

import streamlit as st
import time
import os
import importlib.util

try:
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

def load_module_from_path(name, path):
    if not os.path.exists(path): return None
    try:
        spec = importlib.util.spec_from_file_location(name, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    except Exception as e:
        st.error(f"SYSTEM FAULT: Cannot load {name} -> {e}")
        return None

# The EXACT paths mapped to your screenshots
FILE_MAP = {
    "L01": "anatomy/L01_Anatomical_Manifold.py",
    "L02": "anatomy/L02_Muscular_System.py",
    "L03": "anatomy/L03_Articulations.py",
    "L04": "anatomy/L04_Kinematics.py",
    "L07": "biology/L07_Growth.py",
    "BRAIN": "core/A7DO_Brain.py"
}

# --- INITIALIZATION BOOT SEQUENCE ---
if 'a7do_brain' not in st.session_state:
    modules = {k: load_module_from_path(k, v) for k, v in FILE_MAP.items()}
    if any(v is None for v in modules.values()):
        st.error(f"CRITICAL BOOT FAILURE: Missing files. Ensure {list(FILE_MAP.keys())} are correct.")
        st.stop()

    try:
        skeleton = modules["L01"].BiomechanicalBlueprint()
        muscles = modules["L02"].MuscularBlueprint()
        joints = modules["L03"].ArticulationBlueprint()
        kinematics = modules["L04"].KinematicEngine()
        growth = modules["L07"].MaturationEngine(birth_scale=0.20)
        
        brain = modules["BRAIN"].A7DO_Brain(
            skeleton_manifold=skeleton, muscular_manifold=muscles,
            articulation_manifold=joints, kinematic_engine=kinematics,
            maturation_engine=growth
        )
        st.session_state.a7do_brain = brain
    except Exception as e:
        st.error(f"INITIALIZATION ERROR: {e}")
        st.stop()

brain = st.session_state.a7do_brain

st.set_page_config(page_title="A7DOv12 OS", layout="wide")
st.markdown("""<style>.stMetric { background-color: #161b22; padding: 15px; border-radius: 12px; border: 1px solid #30363d; } .main { background-color: #0d1117; color: #c9d1d9; }</style>""", unsafe_allow_html=True)

with st.sidebar:
    st.title("🛡️ A7DOv12 OS")
    
    st.write("### Motor Cortex Override")
    # Motor controls to manually dictate tension!
    bicep_tension = st.slider("Left Bicep Flexion", 0.0, 1.0, 0.0, 0.1)
    neck_tension = st.slider("Neck Flexion (Nod)", 0.0, 1.0, 0.0, 0.1)
    
    # Send commands to brain BEFORE pulse
    brain.set_muscle_tension("BICEPS_L", bicep_tension)
    brain.set_muscle_tension("STERNOCLEIDOMASTOID_L", neck_tension)
    brain.set_muscle_tension("STERNOCLEIDOMASTOID_R", neck_tension)
    
    state = brain.execute_system_pulse()
    
    st.divider()
    st.subheader(f"Biological Stage: {state['growth']['stage']}")
    st.metric("HEIGHT SCALE (x)", f"{state['growth']['scale_x']:.4f}")

st.title("🦴 Vitruvian Kinematic Manifold")
col1, col2 = st.columns([2, 1])

with col1:
    if PLOTLY_AVAILABLE:
        fig = go.Figure()
        
        # 1. SKELETON
        for b_id, b_data in state["physics"]["skeleton"].items():
            px, py, pz = b_data["proximal"]["x"], b_data["proximal"]["y"], b_data["proximal"]["z"]
            dx, dy, dz = b_data["distal"]["x"], b_data["distal"]["y"], b_data["distal"]["z"]
            fig.add_trace(go.Scatter3d(x=[px, dx], y=[pz, dz], z=[py, dy], mode='lines', line=dict(color='#58a6ff', width=6), hoverinfo='name', name=b_id))

        # 2. JOINTS
        for j_id, j_data in state["physics"]["joints"].items():
            jx, jy, jz = j_data["pos"]["x"], j_data["pos"]["y"], j_data["pos"]["z"]
            fig.add_trace(go.Scatter3d(x=[jx], y=[jz], z=[jy], mode='markers', marker=dict(size=6, color='white', line=dict(color='#58a6ff', width=2)), hoverinfo='name', name=j_id))

        # 3. MUSCLES
        for m_id, m_data in state["physics"]["muscles"].items():
            ox, oy, oz = m_data["origin"]["x"], m_data["origin"]["y"], m_data["origin"]["z"]
            ix, iy, iz = m_data["insertion"]["x"], m_data["insertion"]["y"], m_data["insertion"]["z"]
            
            # Change color to green if muscle is actively tense!
            m_color = '#3fb950' if m_data["tension"] > 0 else 'rgba(255, 80, 80, 0.6)'
            m_width = 5 if m_data["tension"] > 0 else 2
            
            fig.add_trace(go.Scatter3d(x=[ox, ix], y=[oz, iz], z=[oy, iy], mode='lines', line=dict(color=m_color, width=m_width), hoverinfo='name', name=m_id))

        fig.update_layout(margin=dict(l=0, r=0, b=0, t=0), scene=dict(xaxis=dict(range=[-0.5, 0.5], visible=False), yaxis=dict(range=[-0.5, 0.5], visible=False), zaxis=dict(range=[0, 1.1], visible=False), aspectmode='manual', aspectratio=dict(x=1, y=1, z=1.1)), paper_bgcolor='rgba(0,0,0,0)', showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Kinematic Vectors")
    st.info("Notice the Left Bicep vector shorten mathematically as you slide the tension up. The skeleton responds purely to Euclidean coordinates.")
    
    st.write("### Left Arm Math")
    bicep_l = state["physics"]["muscles"]["BICEPS_L"]
    ulna_l = state["physics"]["skeleton"]["RADIUS_ULNA_L"]
    
    st.write(f"**Bicep Tension:** `{bicep_l['tension'] * 100}%`")
    st.write(f"**Forearm Pitch:** `{ulna_l['rotation']['pitch']:.1f}°`")
    st.write(f"**Euclidean Muscle Length:** `{bicep_l['length']:.4f}`")

time.sleep(0.5)
st.rerun()



