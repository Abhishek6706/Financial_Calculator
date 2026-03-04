import pandas as pd


def run_sip_simulation(
    monthly_sip,
    annual_return,
    years,
    step_up,
    inflation
):

    months = years * 12
    monthly_return = annual_return / 12
    monthly_inflation = (1 + inflation) ** (1/12) - 1

    sip = monthly_sip
    corpus = 0

    total_invested = 0
    real_invested = 0

    data = []

    for month in range(1, months + 1):

        corpus = corpus * (1 + monthly_return) + sip

        total_invested += sip

        remaining_months = months - month

        real_value = sip / ((1 + monthly_inflation) ** remaining_months)

        real_invested += real_value

        data.append({
            "month": month,
            "sip": sip,
            "corpus": corpus
        })

        if month % 12 == 0:
            sip = sip * (1 + step_up)

    df = pd.DataFrame(data)

    return df, total_invested, corpus, real_invested, months