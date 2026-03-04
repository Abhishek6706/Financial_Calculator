import streamlit as st
import plotly.graph_objects as go

from engine.sip_engine import run_sip_simulation
from engine.swp_engine import run_swp_simulation
from utils.formatters import format_inr

st.set_page_config(layout="wide")

st.title("Investment Planner")

# Synced Slider + Number Input Function

def synced_slider_input(label, min_val, max_val, default, step=1, key="param"):

    slider_key = f"{key}_slider"
    input_key = f"{key}_input"

    if slider_key not in st.session_state:
        st.session_state[slider_key] = default

    if input_key not in st.session_state:
        st.session_state[input_key] = default

    def update_from_slider():
        st.session_state[input_key] = st.session_state[slider_key]

    def update_from_input():
        st.session_state[slider_key] = st.session_state[input_key]

    col1, col2 = st.columns([3,1])

    with col1:
        st.slider(
            label,
            min_val,
            max_val,
            key=slider_key,
            step=step,
            on_change=update_from_slider
        )

    with col2:
        st.number_input(
            "",
            min_value=min_val,
            max_value=max_val,
            key=input_key,
            step=step,
            on_change=update_from_input
        )

    return st.session_state[slider_key]


# Tabs

tab1, tab2 = st.tabs(["SIP Calculator", "Withdrawal Planner"])


# SIP CALCULATOR

with tab1:

    left, right = st.columns([1.2,1])

    with left:

        monthly_sip = synced_slider_input(
            "Monthly Investment",
            10000,
            50000,
            25000,
            step=1000,
            key="sip"
        )

        expected_return = synced_slider_input(
            "Expected Return (%)",
            8,
            15,
            12,
            key="return"
        )

        years = synced_slider_input(
            "Investment Duration (Years)",
            5,
            20,
            10,
            key="years"
        )

        step_up = synced_slider_input(
            "Annual SIP Step-up (%)",
            5,
            10,
            5,
            key="stepup"
        )

        inflation = synced_slider_input(
            "Inflation Rate (%)",
            4,
            8,
            6,
            key="inflation"
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
            labels=["Invested Amount","Estimated Returns"],
            values=[total_invested,returns],
            hole=.65
        )])

        fig.update_layout(height=400)

        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    col1,col2,col3,col4,col5 = st.columns(5)

    col1.metric("Invested Amount",format_inr(total_invested))
    col2.metric("Est Returns",format_inr(returns))
    col3.metric("Future Corpus",format_inr(corpus))
    col4.metric("Real Invested Value",format_inr(real_invested))
    col5.metric("Real Corpus Value",format_inr(real_corpus))

    st.info(
        f"{format_inr(corpus)} in {years} years will have purchasing power of approximately {format_inr(real_corpus)} today."
    )


# WITHDRAWAL PLANNER

with tab2:

    st.header("Monthly Withdrawal Planner")

    st.metric(
        "Initial Corpus (from SIP)",
        format_inr(corpus)
    )

    st.divider()

    withdrawal = synced_slider_input(
        "Monthly Withdrawal",
        50000,
        100000,
        70000,
        step=1000,
        key="withdraw"
    )

    withdrawal_years = synced_slider_input(
        "Withdrawal Duration (Years)",
        10,
        20,
        15,
        key="withdraw_years"
    )

    withdrawal_return = synced_slider_input(
        "Return During Withdrawal (%)",
        6,
        12,
        10,
        key="withdraw_return"
    )

    withdrawal_return = withdrawal_return / 100

    swp_df, total_withdrawn, remaining = run_swp_simulation(
        corpus,
        withdrawal_return,
        withdrawal,
        withdrawal_years
    )

    st.divider()

    col1,col2 = st.columns(2)

    col1.metric("Total Withdrawn",format_inr(total_withdrawn))
    col2.metric("Remaining Corpus",format_inr(remaining))

    if remaining <= 0:
        st.warning("⚠ Corpus exhausted before withdrawal period ends")
    else:
        st.success("✔ Corpus lasts entire withdrawal duration")