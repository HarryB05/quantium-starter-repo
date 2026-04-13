"""Dash app: Pink Morsel total daily sales around the January 2021 price change."""

from pathlib import Path

import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html

DATA_PATH = Path(__file__).resolve().parent / "data" / "pink_morsel_sales.csv"
PRICE_CHANGE_DATE = pd.Timestamp("2021-01-15")


def load_daily_totals() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH, parse_dates=["Date"])
    totals = (
        df.groupby("Date", as_index=False)["Sales"]
        .sum()
        .sort_values("Date")
        .rename(columns={"Sales": "Total daily sales"})
    )
    return totals


def build_figure():
    daily = load_daily_totals()
    fig = px.line(
        daily,
        x="Date",
        y="Total daily sales",
        labels={
            "Date": "Date",
            "Total daily sales": "Total daily sales ($)",
        },
    )
    fig.update_traces(line=dict(width=2))
    fig.update_layout(
        hovermode="x unified",
        margin=dict(l=48, r=24, t=24, b=48),
    )
    fig.add_vline(
        x=PRICE_CHANGE_DATE,
        line_width=2,
        line_dash="dash",
        line_color="rgba(80,80,80,0.9)",
    )
    fig.add_annotation(
        x=PRICE_CHANGE_DATE,
        y=1.02,
        yref="paper",
        text="Price increase",
        showarrow=False,
        font=dict(size=12),
        xanchor="center",
    )
    return fig


app = Dash(__name__)
app.layout = html.Div(
    [
        html.H1("Soul Foods: Pink Morsel daily sales"),
        html.P(
            "Total sales across all regions, before and after the 15 January 2021 "
            "unit price increase."
        ),
        dcc.Graph(id="sales-chart", figure=build_figure()),
    ],
    style={"maxWidth": "960px", "margin": "0 auto", "padding": "1.5rem"},
)


if __name__ == "__main__":
    app.run(debug=True)
