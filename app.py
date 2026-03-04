import streamlit as st
import plotly.graph_objects as go

from engine.sip_engine import run_sip_simulation
from engine.swp_engine import run_swp_simulation
from utils.formatters import format_inr

st.set_page_config(layout="wide")

st.title("Investment Planner")

tab1, tab2 = st.tabs(["SIP Calculator", "Withdrawal Planner"])

# TAB 1 — SIP CALCULATOR

with tab1:

    left, right = st.columns([1.2, 1])

    with left:

        monthly_sip = st.slider(
            "Monthly Investment",
            10000,
            50000,
            25000,
            step=1000
        )

        expected_return = st.slider(
            "Expected Return (%)",
            8,
            15,
            12
        )

        years = st.slider(
            "Investment Duration (Years)",
            5,
            20,
            10
        )

        step_up = st.slider(
            "Annual SIP Step-up (%)",
            5,
            10,
            5
        )

        inflation = st.slider(
            "Inflation Rate (%)",
            4,
            8,
            6
        )

    expected_return = expected_return / 100
    step_up = step_up / 100
    inflation = inflation / 100

    df, total_invested, corpus, real_invested, months = run_sip_simulation(
        monthly_sip,
        expected_return,
        years,
        step_up,
        inflation
    )

    returns = corpus - total_invested

    monthly_inflation = (1 + inflation) ** (1/12) - 1
    real_corpus = corpus / ((1 + monthly_inflation) ** months)

    with right:

        fig = go.Figure(data=[go.Pie(
            labels=["Invested Amount", "Estimated Returns"],
            values=[total_invested, returns],
            hole=.65
        )])

        fig.update_layout(height=400)

        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric("Invested Amount", format_inr(total_invested))
    col2.metric("Est Returns", format_inr(returns))
    col3.metric("Future Corpus", format_inr(corpus))
    col4.metric("Real Invested Value", format_inr(real_invested))
    col5.metric("Real Corpus Value", format_inr(real_corpus))

    st.info(
        f"{format_inr(corpus)} in {years} years will have purchasing power of approximately {format_inr(real_corpus)} today."
    )

# TAB 2 — WITHDRAWAL PLANNER

with tab2:

    st.header("Monthly Withdrawal Planner")
    
    st.metric(
        "Initial Corpus",
        format_inr(corpus)
    )

    st.divider()

    withdrawal = st.slider(
        "Monthly Withdrawal",
        50000,
        100000,
        70000
    )

    withdrawal_years = st.slider(
        "Withdrawal Duration (Years)",
        10,
        20,
        15
    )

    withdrawal_return = st.slider(
        "Return During Withdrawal (%)",
        6,
        12,
        10
    )

    withdrawal_return = withdrawal_return / 100

    swp_df, total_withdrawn, remaining = run_swp_simulation(
        corpus,
        withdrawal_return,
        withdrawal,
        withdrawal_years
    )

    st.divider()

    col1, col2 = st.columns(2)

    col1.metric(
        "Total Withdrawn",
        format_inr(total_withdrawn)
    )

    col2.metric(
        "Remaining Corpus",
        format_inr(remaining)
    )