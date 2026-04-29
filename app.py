# A7DOv12 Sentience OS
# File: app.py

import importlib.util
import os
import time

import streamlit as st

try:
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False


def load_module_from_path(name, path):
    if not os.path.exists(path):
        return None
    try:
        spec = importlib.util.spec_from_file_location(name, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    except Exception as exc:
        st.error(f"SYSTEM FAULT: Cannot load {name} -> {exc}")
        return None


FILE_MAP = {
    "L01": "anatomy/L01_Anatomical_Manifold.py",
    "L02": "anatomy/L02_Muscular_System.py",
    "L03": "anatomy/L03_Articulations.py",
    "L04": "anatomy/L04_Kinematics.py",
    "L05": "biology/L05_Metabolism.py",
    "L06": "biology/L06_ReflexArc.py",
    "L07": "biology/L07_Growth.py",
    "L08": "biology/L08_Homeostasis.py",
    "L09": "biology/L09_Adaptation.py",
    "BRAIN": "core/A7DO_Brain.py",
}


if "a7do_brain" not in st.session_state:
    modules = {key: load_module_from_path(key, path) for key, path in FILE_MAP.items()}
    if any(value is None for value in modules.values()):
        st.error(f"CRITICAL BOOT FAILURE: Missing files. Ensure {list(FILE_MAP.keys())} are correct.")
        st.stop()

    try:
        skeleton = modules["L01"].BiomechanicalBlueprint()
        muscles = modules["L02"].MuscularBlueprint()
        joints = modules["L03"].ArticulationBlueprint()
        kinematics = modules["L04"].KinematicEngine()
        growth = modules["L07"].MaturationEngine(birth_scale=0.20)

        brain = modules["BRAIN"].A7DO_Brain(
            skeleton_manifold=skeleton,
            muscular_manifold=muscles,
            articulation_manifold=joints,
            kinematic_engine=kinematics,
            maturation_engine=growth,
        )

        st.session_state.a7do_brain = brain
        st.session_state.metabolism = modules["L05"].MetabolicEngine(basal_rate=0.95)
        st.session_state.reflex_arc = modules["L06"].ReflexArc()
        st.session_state.homeostasis = modules["L08"].HomeostasisEngine()
        st.session_state.adaptation = modules["L09"].AdaptationEngine()
        st.session_state.internal_temp = 0.5
    except Exception as exc:
        st.error(f"INITIALIZATION ERROR: {exc}")
        st.stop()

brain = st.session_state.a7do_brain
metabolism = st.session_state.metabolism
reflex_arc = st.session_state.reflex_arc
homeostasis = st.session_state.homeostasis
adaptation = st.session_state.adaptation

st.set_page_config(page_title="A7DOv12 OS", layout="wide")
st.markdown("""<style>.stMetric { background-color: #161b22; padding: 15px; border-radius: 12px; border: 1px solid #30363d; } .main { background-color: #0d1117; color: #c9d1d9; }</style>""", unsafe_allow_html=True)

with st.sidebar:
    st.title("🛡️ A7DOv12 OS")

    st.write("### Motor Cortex Override")
    bicep_tension = st.slider("Left Bicep Flexion", 0.0, 1.0, 0.0, 0.1)
    neck_tension = st.slider("Neck Flexion (Nod)", 0.0, 1.0, 0.0, 0.1)

    st.write("### Bioelectric Stimulus")
    activity_scale = st.slider("Activity Load", 0.2, 2.0, 1.0, 0.1)
    thermal_stress = st.slider("Thermal Stress", 0.0, 1.0, 0.5, 0.05)
    pain_trigger = st.slider("Pain Trigger", 0.0, 1.0, 0.0, 0.1)

    brain.set_muscle_tension("BICEPS_L", bicep_tension)
    brain.set_muscle_tension("STERNOCLEIDOMASTOID_L", neck_tension)
    brain.set_muscle_tension("STERNOCLEIDOMASTOID_R", neck_tension)

    reflex_arc.set_response("PAIN_WITHDRAW", pain_trigger)
    adaptation.record_exposure("PAIN_WITHDRAW")

    state = brain.execute_system_pulse()
    growth = state["growth"]

    energy_demand = metabolism.estimate_energy(growth["mass_x3"], activity_scale=activity_scale)
    st.session_state.internal_temp = homeostasis.stabilize(
        st.session_state.internal_temp,
        thermal_stress,
        correction_gain=0.12,
    )
    adaptation_value = adaptation.adaptation_score("PAIN_WITHDRAW")
    reflex_strength = reflex_arc.get_response("PAIN_WITHDRAW") * (1.0 - adaptation_value)

    st.divider()
    st.subheader(f"Biological Stage: {growth['stage']}")
    st.metric("HEIGHT SCALE (x)", f"{growth['scale_x']:.4f}")
    st.metric("Metabolic Load", f"{energy_demand:.4f}")
    st.metric("Core Temp Scalar", f"{st.session_state.internal_temp:.4f}")
    st.metric("Reflex Output", f"{reflex_strength:.4f}")
    st.metric("Adaptation Score", f"{adaptation_value:.4f}")

st.title("🦴 Vitruvian Kinematic Manifold")
col1, col2 = st.columns([2, 1])

with col1:
    if PLOTLY_AVAILABLE:
        fig = go.Figure()

        for bone_id, bone_data in state["physics"]["skeleton"].items():
            px, py, pz = bone_data["proximal"]["x"], bone_data["proximal"]["y"], bone_data["proximal"]["z"]
            dx, dy, dz = bone_data["distal"]["x"], bone_data["distal"]["y"], bone_data["distal"]["z"]
            fig.add_trace(
                go.Scatter3d(
                    x=[px, dx],
                    y=[pz, dz],
                    z=[py, dy],
                    mode="lines",
                    line=dict(color="#58a6ff", width=6),
                    hoverinfo="name",
                    name=bone_id,
                )
            )

        for joint_id, joint_data in state["physics"]["joints"].items():
            jx, jy, jz = joint_data["pos"]["x"], joint_data["pos"]["y"], joint_data["pos"]["z"]
            fig.add_trace(
                go.Scatter3d(
                    x=[jx],
                    y=[jz],
                    z=[jy],
                    mode="markers",
                    marker=dict(size=6, color="white", line=dict(color="#58a6ff", width=2)),
                    hoverinfo="name",
                    name=joint_id,
                )
            )

        for muscle_id, muscle_data in state["physics"]["muscles"].items():
            ox, oy, oz = muscle_data["origin"]["x"], muscle_data["origin"]["y"], muscle_data["origin"]["z"]
            ix, iy, iz = muscle_data["insertion"]["x"], muscle_data["insertion"]["y"], muscle_data["insertion"]["z"]
            muscle_color = "#3fb950" if muscle_data["tension"] > 0 else "rgba(255, 80, 80, 0.6)"
            muscle_width = 5 if muscle_data["tension"] > 0 else 2
            fig.add_trace(
                go.Scatter3d(
                    x=[ox, ix],
                    y=[oz, iz],
                    z=[oy, iy],
                    mode="lines",
                    line=dict(color=muscle_color, width=muscle_width),
                    hoverinfo="name",
                    name=muscle_id,
                )
            )

        fig.update_layout(
            margin=dict(l=0, r=0, b=0, t=0),
            scene=dict(
                xaxis=dict(range=[-0.5, 0.5], visible=False),
                yaxis=dict(range=[-0.5, 0.5], visible=False),
                zaxis=dict(range=[0, 1.1], visible=False),
                aspectmode="manual",
                aspectratio=dict(x=1, y=1, z=1.1),
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            showlegend=False,
        )
        st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Integrated Physiological Signals")
    st.info("Kinematic output is now connected to metabolic load, reflex modulation, homeostasis, and adaptation memory.")

    bicep_l = state["physics"]["muscles"]["BICEPS_L"]
    ulna_l = state["physics"]["skeleton"]["RADIUS_ULNA_L"]

    st.write(f"**Bicep Tension:** `{bicep_l['tension'] * 100:.1f}%`")
    st.write(f"**Forearm Pitch:** `{ulna_l['rotation']['pitch']:.1f}°`")
    st.write(f"**Euclidean Muscle Length:** `{bicep_l['length']:.4f}`")
    st.write(f"**Energy Demand:** `{energy_demand:.4f}`")
    st.write(f"**Reflex Strength (adapted):** `{reflex_strength:.4f}`")

time.sleep(0.5)
st.rerun()
