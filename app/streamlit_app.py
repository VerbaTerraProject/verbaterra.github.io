import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from verbaterra.sim import SimulationConfig, simulate_block, compute_scores

st.set_page_config(page_title="VerbaTerra vSION Demo", layout="wide")

st.title("VerbaTerra — Cultural–Linguistic Simulation (vSION demo)")
st.caption("Adjust cultural inputs and explore linguistic outcomes (NLIS / CRM).")

with st.sidebar:
    st.header("Cultural Inputs (Means)")
    ritual = st.slider("Ritual Formality (μ)", 1.0, 10.0, 6.7, 0.1)
    trade  = st.slider("Trade Intensity (μ)",  1.0, 10.0, 5.9, 0.1)
    symbol = st.slider("Symbolic Representation (μ)", 1.0, 10.0, 6.3, 0.1)
    hier   = st.slider("Social Hierarchy (μ)", 1.0, 10.0, 6.1, 0.1)
    n      = st.number_input("Population size (n)", 50, 2000, 400, 50)
    sigma  = st.slider("Variance (σ)", 0.5, 3.0, 1.8, 0.1)
    seed   = st.number_input("Random seed", 0, 10_000, 42, 1)
    run = st.button("Run Simulation", type="primary")

cfg = SimulationConfig(n=int(n), ritual_mu=ritual, trade_mu=trade, symbol_mu=symbol, hier_mu=hier, sigma=float(sigma), random_seed=int(seed))

if run:
    base = simulate_block(cfg)
    df = compute_scores(base)

    st.subheader("Summary")
    st.dataframe(df.describe().round(2), use_container_width=True)

    # Plots — NLIS vs CRM, and heatmap-like pair scatter (minimal)
    st.subheader("NLIS vs CRM")
    fig1, ax1 = plt.subplots()
    ax1.scatter(df["NLIS"], df["CRM"], alpha=0.5)
    ax1.set_xlabel("NLIS")
    ax1.set_ylabel("CRM")
    st.pyplot(fig1)

    st.subheader("Cultural Inputs vs Linguistic Outcomes (quick view)")
    cols = st.columns(3)
    with cols[0]:
        fig2, ax2 = plt.subplots()
        ax2.scatter(df["C_ritual"], df["L_syntax"], alpha=0.5)
        ax2.set_xlabel("Ritual (C)")
        ax2.set_ylabel("Syntax (L)")
        st.pyplot(fig2)
    with cols[1]:
        fig3, ax3 = plt.subplots()
        ax3.scatter(df["C_trade"], df["L_lexdiv"], alpha=0.5)
        ax3.set_xlabel("Trade (C)")
        ax3.set_ylabel("Lexical Diversity (L)")
        st.pyplot(fig3)
    with cols[2]:
        fig4, ax4 = plt.subplots()
        ax4.scatter(df["C_symbol"], df["L_semflex"], alpha=0.5)
        ax4.set_xlabel("Symbolism (C)")
        ax4.set_ylabel("Semantic Flexibility (L)")
        st.pyplot(fig4)

    st.download_button(
        "⬇️ Download CSV",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="verbaterra_simulation.csv",
        mime="text/csv",
    )
else:
    st.info("Set your inputs in the sidebar and click **Run Simulation**.")
