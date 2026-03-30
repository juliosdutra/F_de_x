# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 17:36:37 2026
@author: Julio Dutra
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
from datetime import datetime

data_hoje = datetime.now().strftime("%d/%m/%Y")

# =========================
# Funções permitidas
# =========================
allowed_names = {
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

def safe_eval(expr, x):
    """Avaliação com validação básica via SymPy"""
    try:
        sp.sympify(expr)
    except:
        raise ValueError("Expressão inválida")

    local_dict = allowed_names.copy()
    local_dict["x"] = x
    return eval(expr, {"__builtins__": {}}, local_dict)

# =========================
# Interface
# =========================
st.title("📈 Visualizador de Funções")

st.markdown(
"""
Digite uma função de uma variável `x` usando sintaxe do Python.

### 🧠 Exemplos

- `3*x**2`  → $3x^2$  
- `sin(x)`  → $\sin(x)$  
- `exp(-x)*cos(2*x)`  → $e^{-x}\cos(2x)$  
- `sqrt(abs(x))`  → $\sqrt{|x|}$  

---

### ⚠️ Atenção

- Use `*` para multiplicação → `3*x`  
- Use `**` para potência → `x**2`  
- Funções disponíveis: `sin`, `cos`, `tan`, `exp`, `log`, `sqrt`, `abs`

---
"""
)

# Entrada do usuário
expr = st.text_input("Função f(x):", value="sin(x)")

# Conversão para LaTeX
try:
    x_sym = sp.symbols('x')
    expr_sym = sp.sympify(expr)
    st.write("Forma matemática:")
    st.latex(sp.latex(expr_sym))
except:
    st.warning("Expressão não pôde ser convertida para LaTeX")

# Domínio
col1, col2 = st.columns(2)
with col1:
    x_min = st.number_input("x mínimo", value=-10.0)
with col2:
    x_max = st.number_input("x máximo", value=10.0)

num_points = st.slider("Número de pontos", 100, 5000, 500)

# =========================
# Plot
# =========================
if st.button("Plotar função"):

    try:
        x = np.linspace(x_min, x_max, num_points)
        y = safe_eval(expr, x)

        # Tratamento numérico
        y = np.nan_to_num(y, nan=np.nan, posinf=np.nan, neginf=np.nan)

        # Alerta de domínio
        if np.any(np.isnan(y)):
            st.warning("A função possui pontos indefinidos no domínio informado.")

        # Gráfico
        fig, ax = plt.subplots(figsize=(8,4))
        
        ax.axhline(0, color='k')
        ax.axvline(0, color='k')
        
        ax.plot(x, y, label=f"$f(x) = {sp.latex(expr_sym)}$")
        
        
        
        ax.set_xlabel("x")
        ax.set_ylabel("f(x)")
        ax.grid(True)
        ax.legend()

        st.pyplot(fig)
        
    except Exception as e:
        st.error(f"Erro ao avaliar a função: {e}")

# =========================
# Rodapé
# =========================
st.markdown(
    f"""
    <hr style="margin-top:50px;">
    <div style="text-align: center; font-size: 0.9em; color: gray;">
        Desenvolvido por <b>Julio Dutra</b> · Engenharia Química · UFES <br>
        📧 julio.dutra@ufes.br <br>
        📅 {data_hoje}
    </div>
    """,
    unsafe_allow_html=True
)


col1, col2, col3 = st.columns([1,2,1])
with col2:
    st.image(
        "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZDdpaXlqbHA4MXM0N3oydXVvdzRua2VvYWRmamZvODZsNTRmbjYzbCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/7ZoMAYSgQJ8oe5gCYE/giphy.gif",
        width=300
    )