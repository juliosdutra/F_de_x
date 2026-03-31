# -*- coding: utf-8 -*-
"""
Visualizador de Funções - Versão com Plotly
@author: Julio Dutra
"""

import streamlit as st
import numpy as np
import sympy as sp
from datetime import datetime
import webbrowser
import plotly.graph_objects as go

# =========================
# Configuração da página
# =========================
st.set_page_config(page_title="Visualizador de Funções", layout="wide")

# =========================
# Funções permitidas
# =========================
ALLOWED = {
    "x": None,
    "sin": np.sin,
    "cos": np.cos,
    "tan": np.tan,
    "exp": np.exp,
    "log": np.log,
    "sqrt": np.sqrt,
    "pi": np.pi,
    "abs": np.abs
}

# =========================
# Funções auxiliares
# =========================
@st.cache_data
def gerar_dados(expr, x_min, x_max, n):
    x = np.linspace(x_min, x_max, n)
    y = avaliar(expr, x)
    return x, y

def avaliar(expr, x):
    try:
        sp.sympify(expr)
    except:
        raise ValueError("Expressão inválida")

    local = ALLOWED.copy()
    local["x"] = x

    y = eval(expr, {"__builtins__": {}}, local)

    return np.nan_to_num(y, nan=np.nan, posinf=np.nan, neginf=np.nan)

def encontrar_zeros(x, y):
    zeros = []
    for i in range(len(y) - 1):
        if np.sign(y[i]) != np.sign(y[i+1]) and y[i+1] != y[i]:
            x0 = x[i] - y[i] * (x[i+1] - x[i]) / (y[i+1] - y[i])
            zeros.append(x0)
    return zeros

def plotar_funcao_plotly(x, y, expr_sym, zeros, mostrar_zeros):
    fig = go.Figure()

    # Curva principal
    label = "f(x)"

    fig.add_trace(go.Scatter(
        x=x,
        y=y,
        mode='lines',
        name=label
    ))

    # Eixos
    fig.add_hline(y=0, line_width=1)
    fig.add_vline(x=0, line_width=1)

    # Zeros
    if mostrar_zeros and zeros:
        fig.add_trace(go.Scatter(
            x=zeros,
            y=[0]*len(zeros),
            mode='markers',
            name='Zeros',
            marker=dict(size=8)
        ))

    fig.update_layout(
        xaxis_title="x",
        yaxis_title="f(x)",
        template="plotly_white",
        hovermode="closest"
    )

    return fig

# =========================
# SIDEBAR
# =========================
st.sidebar.markdown("**Engenharia Química - UFES (Alegre)**")
st.sidebar.markdown("---")

expr = st.sidebar.text_input("Função f(x):", " sin(x) * exp(-0.1*x**2) + 0.3*cos(3*x)")

x_min = st.sidebar.number_input("x mínimo", value=-10.0)
x_max = st.sidebar.number_input("x máximo", value=10.0)

num_points = st.sidebar.slider("Número de pontos", 100, 5000, 500)

mostrar_zeros = st.sidebar.checkbox("Mostrar zeros", True)

st.sidebar.markdown("---")

col1, col2, col3 = st.sidebar.columns([1, 2, 1])
with col2:
    if st.button("🌐 Acessar UFES"):
        webbrowser.open("https://www.ufes.br")

    st.markdown(
        f"""
        <hr>
        <div style="text-align:center; font-size:0.9em; color:gray;">
        Julio Dutra · julio.dutra@ufes.br  </div>
        """,
        unsafe_allow_html=True
    )



# =========================
# MAIN
# =========================
st.title("📈 Visualizador de Funções (Plotly)")

# ---- LaTeX ----
expr_sym = None
try:
    x_sym = sp.symbols('x')
    expr_sym = sp.sympify(expr)

    st.markdown("### 📐 Expressão matemática")
    st.latex(sp.latex(expr_sym))

except:
    st.warning("Expressão inválida")

# ---- Processamento ----
try:
    with st.spinner("Calculando..."):
        x, y = gerar_dados(expr, x_min, x_max, num_points)

    if np.any(np.isnan(y)):
        st.warning("A função possui pontos indefinidos no domínio.")

    zeros = encontrar_zeros(x, y)

    # ---- Plot ----
    st.markdown("### 📊 Gráfico")
    col1, col2, col3 = st.columns([1, 4, 1])

    with col2:
        fig = plotar_funcao_plotly(x, y, expr_sym, zeros, mostrar_zeros)
        st.plotly_chart(fig, use_container_width=True)

    # ---- Zeros ----
    if mostrar_zeros:
        if zeros:
            st.markdown("### 📍 Zeros aproximados")
            st.write([round(z, 4) for z in zeros])
        else:
            st.info("Nenhum zero encontrado no intervalo.")

    st.toast("Gráfico atualizado", icon="📈")

except Exception as e:
    st.error(f"Erro: {e}")

# =========================
# Rodapé
# =========================
data = datetime.now().strftime("%d/%m/%Y")

st.markdown(
    f"""
    <hr>
    <div style="text-align:center; font-size:0.9em; color:gray;">
    Julio Dutra · UFES · julio.dutra@ufes.br · {data}
    </div>
    """,
    unsafe_allow_html=True
)