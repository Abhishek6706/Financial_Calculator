import pandas as pd


def run_swp_simulation(
    corpus,
    annual_return,
    withdrawal,
    years
):

    months = years * 12
    monthly_return = annual_return / 12

    total_withdrawn = 0

    data = []

    for month in range(1, months + 1):

        corpus = corpus * (1 + monthly_return)

        if corpus >= withdrawal:
            corpus -= withdrawal
            total_withdrawn += withdrawal
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