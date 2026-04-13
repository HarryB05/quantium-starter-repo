"""Dash app: Pink Morsel daily sales with region filter and styled layout."""

from pathlib import Path

import pandas as pd
import plotly.express as px
from dash import Dash, Input, Output, callback, dcc, html

DATA_PATH = Path(__file__).resolve().parent / "data" / "pink_morsel_sales.csv"
PRICE_CHANGE_DATE = pd.Timestamp("2021-01-15")

COLOR_PAGE_TEXT = "#2c2824"
COLOR_LINE = "#2d6a4f"
COLOR_VLINE = "#b85c38"
COLOR_GRID = "#e5e0d8"
COLOR_PLOT_BG = "#faf8f5"


def load_transactions() -> pd.DataFrame:
    return pd.read_csv(DATA_PATH, parse_dates=["Date"])


def aggregate_daily(region: str) -> pd.DataFrame:
    df = load_transactions()
    if region != "all":
        df = df[df["Region"] == region]
    return (
        df.groupby("Date", as_index=False)["Sales"]
        .sum()
        .sort_values("Date")
    )


def build_figure(region: str):
    daily = aggregate_daily(region)
    y_title = (
        "Total daily sales ($)" if region == "all" else "Daily sales, region ($)"
    )
    fig = px.line(
        daily,
        x="Date",
        y="Sales",
        labels={"Date": "Date", "Sales": y_title},
    )
    fig.update_traces(line=dict(width=2.5, color=COLOR_LINE))
    fig.update_layout(
        hovermode="x unified",
        margin=dict(l=56, r=28, t=36, b=52),
        paper_bgcolor=COLOR_PLOT_BG,
        plot_bgcolor=COLOR_PLOT_BG,
        font=dict(color=COLOR_PAGE_TEXT, family="DM Sans, Segoe UI, system-ui, sans-serif"),
        xaxis=dict(
            showgrid=True,
            gridcolor=COLOR_GRID,
            zeroline=False,
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor=COLOR_GRID,
            zeroline=False,
        ),
    )
    fig.add_vline(
        x=PRICE_CHANGE_DATE,
        line_width=2,
        line_dash="dash",
        line_color=COLOR_VLINE,
    )
    fig.add_annotation(
        x=PRICE_CHANGE_DATE,
        y=1.02,
        yref="paper",
        text="Price increase",
        showarrow=False,
        font=dict(size=12, color=COLOR_PAGE_TEXT),
        xanchor="center",
    )
    return fig


app = Dash(__name__)
app.layout = html.Div(
    className="app-shell",
    children=[
        html.Header(
            className="app-header",
            children=[
                html.H1("Soul Foods: Pink Morsel daily sales", className="app-title"),
                html.P(
                    "Explore total or region-specific sales before and after the "
                    "15 January 2021 unit price increase. Use the control below to "
                    "narrow the chart.",
                    className="app-lede",
                ),
            ],
        ),
        html.Div(
            className="region-panel",
            children=[
                html.Span("Region", className="region-panel__label"),
                dcc.RadioItems(
                    id="region-filter",
                    options=[
                        {"label": "All", "value": "all"},
                        {"label": "North", "value": "north"},
                        {"label": "East", "value": "east"},
                        {"label": "South", "value": "south"},
                        {"label": "West", "value": "west"},
                    ],
                    value="all",
                    className="region-radio",
                    labelClassName="region-radio__label",
                    inputClassName="region-radio__input",
                ),
            ],
        ),
        html.Div(
            className="chart-card",
            children=[
                dcc.Graph(id="sales-chart", figure=build_figure("all")),
            ],
        ),
    ],
)


@callback(
    Output("sales-chart", "figure"),
    Input("region-filter", "value"),
)
def update_sales_chart(region: str):
    return build_figure(region)


if __name__ == "__main__":
    app.run(debug=True)
