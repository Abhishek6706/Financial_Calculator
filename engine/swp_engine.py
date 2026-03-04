import pandas as pd


def run_swp_simulation(
    corpus: float,
    annual_return: float,
    monthly_withdrawal: float,
    years: int
):

    months = years * 12
    monthly_return = annual_return / 12

    data = []

    total_withdrawn = 0

    for month in range(1, months + 1):

        corpus = corpus * (1 + monthly_return)

        if corpus >= monthly_withdrawal:
            corpus -= monthly_withdrawal
            total_withdrawn += monthly_withdrawal
        else:
            total_withdrawn += corpus
            corpus = 0

        data.append({
            "month": month,
            "corpus": corpus
        })

        if corpus <= 0:
            break

    df = pd.DataFrame(data)

    return df, total_withdrawn, corpus