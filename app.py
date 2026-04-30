# app.py
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import time

from engine.organism import Organism


# -----------------------------
# INIT SYSTEM (PERSISTENT)
# -----------------------------
if "org" not in st.session_state:
    st.session_state.org = Organism()

org = st.session_state.org


# -----------------------------
# UI
# -----------------------------
st.title("🧠 A7DO – Life Engine (2D Structure Mode)")

col1, col2 = st.columns(2)

steps = col1.slider("Simulation Steps", 1, 50, 10)
dt = col2.slider("Speed (dt)", 0.01, 0.5, 0.1)

run = st.button("Run Simulation Step")


# -----------------------------
# RUN SIMULATION
# -----------------------------
if run:
    for _ in range(steps):
        org.update(dt)


# -----------------------------
# VITALS
# -----------------------------
st.subheader("Vitals")

st.write({
    "time": round(org.time, 2),
    "cell_count": len(org.cells),
})


# -----------------------------
# BUILD SIMPLE SKELETON
# -----------------------------
def build_simple_skeleton(cells):
    positions = np.array([c.position for c in cells])

    if len(positions) == 0:
        return {}

    # Spine (vertical sampling)
    spine = []
    y_vals = np.linspace(positions[:,1].min(), positions[:,1].max(), 12)

    for y in y_vals:
        close = positions[np.abs(positions[:,1] - y) < 0.5]
        if len(close) > 0:
            spine.append(close.mean(axis=0))

    # Head (top cluster)
    head = positions[positions[:,1] > positions[:,1].max() - 2]

    # Arms (side clusters)
    left_arm = positions[positions[:,0] < -1]
    right_arm = positions[positions[:,0] > 1]

    return {
        "spine": spine,
        "head": head,
        "left_arm": left_arm,
        "right_arm": right_arm
    }


# -----------------------------
# 2D VISUAL
# -----------------------------
st.subheader("2D Body Structure")

skeleton = build_simple_skeleton(org.cells)

fig, ax = plt.subplots()

# --- Draw Spine ---
if "spine" in skeleton and len(skeleton["spine"]) > 0:
    spine = skeleton["spine"]
    xs = [p[0] for p in spine]
    ys = [p[1] for p in spine]
    ax.plot(xs, ys, linewidth=3)

# --- Draw Head ---
if "head" in skeleton and len(skeleton["head"]) > 0:
    h = skeleton["head"]
    ax.scatter(h[:,0], h[:,1], s=10)

# --- Draw Arms ---
if "left_arm" in skeleton and len(skeleton["left_arm"]) > 0:
    la = skeleton["left_arm"]
    ax.scatter(la[:,0], la[:,1], s=5)

if "right_arm" in skeleton and len(skeleton["right_arm"]) > 0:
    ra = skeleton["right_arm"]
    ax.scatter(ra[:,0], ra[:,1], s=5)

# --- Optional: show raw cells (faint background) ---
show_cells = st.checkbox("Show Raw Cells", value=False)

if show_cells:
    xs = [c.position[0] for c in org.cells]
    ys = [c.position[1] for c in org.cells]
    ax.scatter(xs, ys, s=2, alpha=0.2)

# Layout
ax.set_xlim(-20, 20)
ax.set_ylim(-5, 30)

st.pyplot(fig)