
import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Simulasi RLC Seri Lengkap", layout="wide")
st.title("⚡ Visualisasi Interaktif & Analisis Rangkaian RLC Seri")

# ---------------- PARAMETER INPUT ----------------
st.sidebar.header("🔧 Parameter RLC")
R = st.sidebar.slider("Resistansi R (Ω)", 1.0, 100.0, 10.0)
L = st.sidebar.slider("Induktansi L (H)", 0.001, 1.0, 0.1)
C = st.sidebar.slider("Kapasitansi C (F)", 0.000001, 0.01, 0.001)
E0 = st.sidebar.slider("Amplitudo Tegangan E₀ (V)", 1.0, 100.0, 10.0)
f = st.sidebar.slider("Frekuensi f (Hz)", 0.1, 100.0, 50.0)

# ---------------- PERHITUNGAN ----------------
ω = 2 * np.pi * f
XL = ω * L
XC = 1 / (ω * C)
Z = np.sqrt(R**2 + (XL - XC)**2)
I0 = E0 / Z
phi = np.arctan2((XL - XC), R)
Q = ω * L / R
f0 = 1 / (2 * np.pi * np.sqrt(L * C))

t = np.linspace(0, 0.1, 1000)
i_t = I0 * np.sin(ω * t - phi)
v_t = E0 * np.sin(ω * t)
p_t = v_t * i_t

# ---------------- VISUALISASI RANGKAIAN ----------------
st.subheader("🧩 Rangkaian RLC Seri: Visualisasi 2D")

fig = go.Figure()

# Garis kabel putih
fig.add_trace(go.Scatter(x=[0, 8], y=[0, 0], mode='lines', line=dict(color='white', width=3)))
fig.add_trace(go.Scatter(x=[8, 8], y=[0, 2], mode='lines', line=dict(color='white', width=3)))
fig.add_trace(go.Scatter(x=[8, 0], y=[2, 2], mode='lines', line=dict(color='white', width=3)))
fig.add_trace(go.Scatter(x=[0, 0], y=[2, 0], mode='lines', line=dict(color='white', width=3)))

# Titik komponen dengan hoverinfo
komponen = [
    {"x": [0.5], "y": [2], "label": "R", "hover": "Resistor\nR = {:.2f} Ω".format(R), "color": "red"},
    {"x": [3], "y": [2], "label": "L", "hover": "Induktor\nL = {:.4f} H".format(L), "color": "blue"},
    {"x": [5.5], "y": [2], "label": "C", "hover": "Kapasitor\nC = {:.6f} F".format(C), "color": "green"},
    {"x": [0], "y": [1], "label": "V", "hover": "Sumber AC\nE₀ = {:.2f} V".format(E0), "color": "magenta"}
]

for k in komponen:
    fig.add_trace(go.Scatter(
        x=k["x"], y=k["y"], mode="markers+text",
        marker=dict(color=k["color"], size=10),
        text=[k["label"]],
        textposition="middle center",
        textfont=dict(color="white", size=16),
        hoverinfo="text",
        hovertext=k["hover"],
        showlegend=False
    ))

fig.update_layout(
    showlegend=False,
    xaxis=dict(visible=False),
    yaxis=dict(visible=False),
    plot_bgcolor="black",
    paper_bgcolor="black",
    height=450,
    width=900
)

st.plotly_chart(fig, use_container_width=True)

# ---------------- GRAFIK ----------------
st.subheader("📊 Analisis Gelombang Tegangan, Arus, dan Daya")

col1, col2 = st.columns(2)

with col1:
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=t, y=v_t, name="Tegangan (V)", line=dict(color="magenta")))
    fig1.add_trace(go.Scatter(x=t, y=i_t, name="Arus (A)", line=dict(color="orange")))
    fig1.update_layout(title="Tegangan & Arus vs Waktu", xaxis_title="Waktu (s)", yaxis_title="Amplitudo")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=t, y=p_t, name="Daya (P = V × I)", line=dict(color="cyan")))
    fig2.update_layout(title="Daya Sesaat vs Waktu", xaxis_title="Waktu (s)", yaxis_title="Daya (W)")
    st.plotly_chart(fig2, use_container_width=True)

# ---------------- OUTPUT ----------------
st.subheader("📌 Hasil Perhitungan Rangkaian")
st.markdown(f"""
- **Frekuensi Sudut (ω)** = {ω:.2f} rad/s  
- **Impedansi Total (Z)** = {Z:.2f} Ω  
- **Reaktansi Induktor (Xᴸ)** = {XL:.2f} Ω  
- **Reaktansi Kapasitor (Xᶜ)** = {XC:.2f} Ω  
- **Arus Maksimum (I₀)** = {I0:.2f} A  
- **Sudut Fase (φ)** = {np.degrees(phi):.2f}°  
- **Faktor Kualitas (Q)** = {Q:.2f}  
- **Frekuensi Resonansi (f₀)** = {f0:.2f} Hz  
- **Daya Rata-rata** = {(0.5 * E0 * I0 * np.cos(phi)):.2f} W  
""")
