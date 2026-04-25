
# A7DOv12 Sentience OS - Fresh Build
# File 5: app.py
# Purpose: The Visual Dashboard and Render Engine.
# Logic: Zero math. Pure rendering of A7DO_Brain outputs.

import streamlit as st
import time
import os
import importlib.util
import plotly.graph_objects as go

# --- SYSTEM DIAGNOSTICS & PLOTLY CHECK ---
try:
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

# --- SECURE DYNAMIC LOADER ---
# Bypasses standard imports to strictly enforce our file architecture
def load_module_from_path(name, path):
    if not os.path.exists(path):
        return None
    try:
        spec = importlib.util.spec_from_file_location(name, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    except Exception as e:
        st.error(f"SYSTEM FAULT: Cannot load {name} -> {e}")
        return None

# The absolute paths for our new deterministic A7DOv12 structure
FILE_MAP = {
    "L01": "a7do_system/anatomy/L01_Skeleton.py",
    "L02": "a7do_system/anatomy/L02_Muscles.py",
    "L07": "a7do_system/biology/L07_Growth.py",
    "BRAIN": "a7do_system/core/A7DO_Brain.py"
}

# --- INITIALIZATION BOOT SEQUENCE ---
if 'a7do_brain' not in st.session_state:
    st.session_state.boot_log = {}
    modules = {k: load_module_from_path(k, v) for k, v in FILE_MAP.items()}
    
    # Check for missing files
    missing = [k for k, v in modules.items() if v is None]
    if missing:
        st.error(f"CRITICAL BOOT FAILURE: Missing files {missing}. Please check 'a7do_system' folder structure.")
        st.stop()

    # Initialize the specific biological objects
    try:
        skeleton = modules["L01"].SkeletalManifold()
        muscles = modules["L02"].MuscularBlueprint()
        growth = modules["L07"].MaturationEngine(birth_scale=0.20)
        
        # Inject them into the Central Nervous System
        brain = modules["BRAIN"].A7DO_Brain(
            skeleton_manifold=skeleton,
            muscular_manifold=muscles,
            maturation_engine=growth
        )
        st.session_state.a7do_brain = brain
    except Exception as e:
        st.error(f"INITIALIZATION ERROR: {e}")
        st.stop()

# --- THE MASTER PULSE ---
# The app asks the Brain for the absolute state for this single frame
brain = st.session_state.a7do_brain
state = brain.execute_system_pulse()

# --- UI STYLING ---
st.set_page_config(page_title="A7DOv12 OS", layout="wide")
st.markdown("""
<style>
    .stMetric { background-color: #161b22; padding: 15px; border-radius: 12px; border: 1px solid #30363d; }
    .main { background-color: #0d1117; color: #c9d1d9; }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR: DETERMINISTIC TELEMETRY ---
with st.sidebar:
    st.title("🛡️ A7DOv12 OS")
    st.caption("Strict Biomechanical Math Engine")
    
    st.subheader(f"Biological Stage: {state['growth']['stage']}")
    st.metric("HEIGHT SCALE (x)", f"{state['growth']['scale_x']:.4f}")
    st.metric("MASS PENALTY (x³)", f"{state['growth']['mass_x3']:.4f}")
    
    st.divider()
    st.write("### Da Vinci Proportions")
    st.write(f"**Head Ratio:** `1 / {round(1/state['growth']['head_ratio'], 1)}`")
    st.write(f"**Limb Stretch:** `{round(state['growth']['limb_ratio']*100, 1)}%`")
    
    st.divider()
    st.write("### Developmental Log")
    for log in reversed(state.get("logs", [])):
        st.caption(f"[{log['height_scalar']}x] Transitioned to {log['stage']}")

# --- MAIN DASHBOARD: 3D RENDER ENGINE ---
st.title("🦴 Vitruvian Synthesis Manifold")

col1, col2 = st.columns([2, 1])

with col1:
    if PLOTLY_AVAILABLE:
        fig = go.Figure()
        
        # 1. DRAW SKELETON (Using Proximal and Distal ends from L01)
        bones = state["physics"]["skeleton"]
        for b_id, b_data in bones.items():
            px, py, pz = b_data["proximal"]["x"], b_data["proximal"]["y"], b_data["proximal"]["z"]
            dx, dy, dz = b_data["distal"]["x"], b_data["distal"]["y"], b_data["distal"]["z"]
            cx, cy, cz = b_data["center"]["x"], b_data["center"]["y"], b_data["center"]["z"]
            
            # Draw the bone as a solid line
            fig.add_trace(go.Scatter3d(
                x=[px, dx], y=[pz, dz], z=[py, dy], # Swap Y/Z for correct upright viewing
                mode='lines+markers',
                line=dict(color='#58a6ff', width=8),
                marker=dict(size=4, color='white'),
                name=f"Bone: {b_id}",
                hoverinfo='name'
            ))

        # 2. DRAW MUSCLES (Using Origin and Insertion from L02)
        muscles = state["physics"]["muscles"]
        for m_id, m_data in muscles.items():
            ox, oy, oz = m_data["origin"]["x"], m_data["origin"]["y"], m_data["origin"]["z"]
            ix, iy, iz = m_data["insertion"]["x"], m_data["insertion"]["y"], m_data["insertion"]["z"]
            
            # Draw the muscle as a thinner red vector
            fig.add_trace(go.Scatter3d(
                x=[ox, ix], y=[oz, iz], z=[oy, iy],
                mode='lines',
                line=dict(color='rgba(255, 80, 80, 0.6)', width=3),
                name=f"Actuator: {m_id}",
                hoverinfo='name'
            ))

        # Lock the 3D Room size so the camera doesn't zoom in/out as he grows.
        # This makes the growth visually obvious!
        fig.update_layout(
            margin=dict(l=0, r=0, b=0, t=0),
            scene=dict(
                xaxis=dict(range=[-0.5, 0.5], visible=False),
                yaxis=dict(range=[-0.5, 0.5], visible=False),
                zaxis=dict(range=[0, 1.1], visible=False), # Floor to Ceiling
                aspectmode='manual',
                aspectratio=dict(x=1, y=1, z=1.1)
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("Plotly engine missing. Please ensure `plotly` is in requirements.txt")

with col2:
    st.subheader("Physics Telemetry")
    st.info("The rendering engine utilizes absolute Euclidean coordinates passed down from the Central Nervous System.")
    
    st.write("### Active Actuators (Muscles)")
    with st.container(height=300):
        for m_id, m_data in state["physics"]["muscles"].items():
            st.write(f"`{m_id}` | Len: {m_data['length']:.3f}")

# Trigger next pulse
time.sleep(0.5)
st.rerun()

