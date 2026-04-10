import pandas as pd
import plotly.express as px
from dash import Dash, Input, Output, dcc, html


DATA_PATH = "./output.csv"
PRICE_INCREASE_DATE = pd.Timestamp("2021-01-15")
REGION_OPTIONS = [
    {"label": "All", "value": "all"},
    {"label": "North", "value": "north"},
    {"label": "East", "value": "east"},
    {"label": "South", "value": "south"},
    {"label": "West", "value": "west"},
]


def load_sales_data() -> pd.DataFrame:
    sales_data = pd.read_csv(DATA_PATH, parse_dates=["Date"])
    sales_data["Region"] = sales_data["Region"].str.lower()
    return sales_data.sort_values("Date")


def build_daily_sales(sales_data: pd.DataFrame, region: str) -> pd.DataFrame:
    filtered_sales = sales_data if region == "all" else sales_data[sales_data["Region"] == region]
    daily_sales = ( filtered_sales.groupby("Date", as_index=False)["Sales"].sum().sort_values("Date") )
    daily_sales["Period"] = daily_sales["Date"].apply(
        lambda date: "Before price increase"
        if date < PRICE_INCREASE_DATE
        else "After price increase"
    )
    return daily_sales


def build_figure(daily_sales: pd.DataFrame, region: str):
    region_label = "All Regions" if region == "all" else region.title()
    figure = px.line(
        daily_sales,
        x="Date",
        y="Sales",
        color="Period",
        color_discrete_map={
            "Before price increase": "#ffb703",
            "After price increase": "#fb5607",
        },
        labels={"Date": "Date", "Sales": "Total sales ($)", "Period": ""},
        title=f"Pink Morsel Daily Sales: {region_label}",
    )

    figure.update_traces(line={"width": 4})
    figure.update_layout(
        plot_bgcolor="rgba(8, 15, 33, 0)",
        paper_bgcolor="rgba(8, 15, 33, 0)",
        hovermode="x unified",
        legend={"orientation": "h", "y": 1.08, "x": 0, "bgcolor": "rgba(0,0,0,0)"},
        margin={"l": 30, "r": 30, "t": 72, "b": 30},
        font={"family": "Segoe UI, sans-serif", "color": "#f8fafc"},
        title={"font": {"size": 24}},
    )
    figure.update_xaxes(
        showgrid=False,
        linecolor="rgba(255,255,255,0.25)",
        tickfont={"color": "#cbd5e1"},
    )
    figure.update_yaxes(
        gridcolor="rgba(255,255,255,0.14)",
        zeroline=False,
        tickprefix="$",
        tickfont={"color": "#cbd5e1"},
    )
    figure.add_shape(
        type="line",
        x0=PRICE_INCREASE_DATE,
        x1=PRICE_INCREASE_DATE,
        y0=0,
        y1=1,
        xref="x",
        yref="paper",
        line={"dash": "dash", "color": "#e2e8f0", "width": 2},
    )
    figure.add_annotation(
        x=PRICE_INCREASE_DATE,
        y=1,
        xref="x",
        yref="paper",
        text="Price increase: 15 Jan 2021",
        showarrow=False,
        xanchor="left",
        yanchor="bottom",
        bgcolor="rgba(15, 23, 42, 0.85)",
        bordercolor="rgba(255,255,255,0.18)",
        font={"color": "#f8fafc"},
    )
    return figure


sales_data = load_sales_data()
initial_daily_sales = build_daily_sales(sales_data, "all")

app = Dash(__name__)
app.title = "Soul Foods Sales Visualiser"

app.layout = html.Div(
    className="page-shell",
    children=[
        html.Div(
            className="hero-card",
            children=[
                html.Div(
                    className="hero-copy",
                    children=[
                        html.P("Soul Foods Analytics", className="eyebrow"),
                        html.H1("Pink Morsel Sales Visualiser"),
                        html.P("Daily Pink Morsel sales jump after the 15 January 2021 price increase."),
                    ],
                ),
            ],
        ),
        html.Div(
            className="dashboard-card",
            children=[
                html.Div(
                    className="controls-row",
                    children=[
                        html.Div(
                            className="control-panel",
                            children=[
                                html.Label("Filter by region", className="control-label"),
                                dcc.RadioItems(
                                    id="region-filter",
                                    options=REGION_OPTIONS,
                                    value="all",
                                    className="region-radio-group",
                                    inputClassName="region-radio-input",
                                    labelClassName="region-radio-label",
                                ),
                            ],
                        ),
                    ],
                ),
                dcc.Graph(
                    id="sales-line-chart",
                    figure=build_figure(initial_daily_sales, "all"),
                    className="chart-panel",
                    config={"displayModeBar": False},
                ),
            ],
        ),
    ],
)


@app.callback( Output("sales-line-chart", "figure"), Input("region-filter", "value") )

def update_dashboard(region: str):
    daily_sales = build_daily_sales(sales_data, region)
    return build_figure(daily_sales, region)

if __name__ == "__main__": app.run(debug=True)