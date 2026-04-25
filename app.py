
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

FILE_MAP = {
    "L01": "anatomy/L01_Anatomical_Manifold.py",
    "L02": "anatomy/L02_Muscular_System.py",
    "L03": "anatomy/L03_Articulations.py",
    "L07": "biology/L07_Growth.py",
    "BRAIN": "core/A7DO_Brain.py"
}

if 'a7do_brain' not in st.session_state:
    modules = {k: load_module_from_path(k, v) for k, v in FILE_MAP.items()}
    if any(v is None for v in modules.values()):
        st.error("CRITICAL BOOT FAILURE: Missing files. Ensure L03_Articulations.py is saved.")
        st.stop()

    try:
        skeleton = modules["L01"].BiomechanicalBlueprint()
        muscles = modules["L02"].MuscularBlueprint()
        joints = modules["L03"].ArticulationBlueprint()
        growth = modules["L07"].MaturationEngine(birth_scale=0.20)
        
        brain = modules["BRAIN"].A7DO_Brain(
            skeleton_manifold=skeleton, muscular_manifold=muscles,
            articulation_manifold=joints, maturation_engine=growth
        )
        st.session_state.a7do_brain = brain
    except Exception as e:
        st.error(f"INITIALIZATION ERROR: {e}")
        st.stop()

brain = st.session_state.a7do_brain
state = brain.execute_system_pulse()

st.set_page_config(page_title="A7DOv12 OS", layout="wide")
st.markdown("""<style>.stMetric { background-color: #161b22; padding: 15px; border-radius: 12px; border: 1px solid #30363d; } .main { background-color: #0d1117; color: #c9d1d9; }</style>""", unsafe_allow_html=True)

with st.sidebar:
    st.title("🛡️ A7DOv12 OS")
    st.subheader(f"Stage: {state['growth']['stage']}")
    st.metric("HEIGHT SCALE (x)", f"{state['growth']['scale_x']:.4f}")
    st.metric("MASS PENALTY (x³)", f"{state['growth']['mass_x3']:.4f}")
    st.divider()
    st.write("### Developmental Log")
    for log in reversed(state.get("logs", [])):
        st.caption(f"[{log['height_scalar']}x] Transitioned to {log['stage']}")

st.title("🦴 Vitruvian Synthesis Manifold")
col1, col2 = st.columns([2, 1])

with col1:
    if PLOTLY_AVAILABLE:
        fig = go.Figure()
        
        # 1. SKELETON (Blue Lines)
        for b_id, b_data in state["physics"]["skeleton"].items():
            px, py, pz = b_data["proximal"]["x"], b_data["proximal"]["y"], b_data["proximal"]["z"]
            dx, dy, dz = b_data["distal"]["x"], b_data["distal"]["y"], b_data["distal"]["z"]
            fig.add_trace(go.Scatter3d(x=[px, dx], y=[pz, dz], z=[py, dy], mode='lines', line=dict(color='#58a6ff', width=6), hoverinfo='name', name=b_id))

        # 2. JOINTS (White Glowing Nodes)
        for j_id, j_data in state["physics"]["joints"].items():
            jx, jy, jz = j_data["pos"]["x"], j_data["pos"]["y"], j_data["pos"]["z"]
            fig.add_trace(go.Scatter3d(x=[jx], y=[jz], z=[jy], mode='markers', marker=dict(size=6, color='white', line=dict(color='#58a6ff', width=2)), hoverinfo='name', name=j_id))

        # 3. MUSCLES (Red Vectors)
        for m_id, m_data in state["physics"]["muscles"].items():
            ox, oy, oz = m_data["origin"]["x"], m_data["origin"]["y"], m_data["origin"]["z"]
            ix, iy, iz = m_data["insertion"]["x"], m_data["insertion"]["y"], m_data["insertion"]["z"]
            fig.add_trace(go.Scatter3d(x=[ox, ix], y=[oz, iz], z=[oy, iy], mode='lines', line=dict(color='rgba(255, 80, 80, 0.6)', width=2), hoverinfo='name', name=m_id))

        fig.update_layout(margin=dict(l=0, r=0, b=0, t=0), scene=dict(xaxis=dict(range=[-0.5, 0.5], visible=False), yaxis=dict(range=[-0.5, 0.5], visible=False), zaxis=dict(range=[0, 1.1], visible=False), aspectmode='manual', aspectratio=dict(x=1, y=1, z=1.1)), paper_bgcolor='rgba(0,0,0,0)', showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Joint Articulations")
    with st.container(height=200):
        for j_id, j_data in state["physics"]["joints"].items():
            st.write(f"⚙️ **{j_id}** (`{j_data['type']}`)")
            
    st.subheader("Active Actuators")
    with st.container(height=300):
        for m_id, m_data in state["physics"]["muscles"].items():
            st.write(f"🔴 `{m_id}` | Len: {m_data['length']:.3f}")

time.sleep(0.5)
st.rerun()



