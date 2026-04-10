import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html


DATA_PATH = "./output.csv"
PRICE_INCREASE_DATE = pd.Timestamp("2021-01-15")


def load_daily_sales() -> pd.DataFrame:
    sales_data = pd.read_csv(DATA_PATH, parse_dates=["Date"])
    daily_sales = (
        sales_data.groupby("Date", as_index=False)["Sales"]
        .sum()
        .sort_values("Date")
    )
    daily_sales["Period"] = daily_sales["Date"].apply(
        lambda date: "Before price increase"
        if date < PRICE_INCREASE_DATE
        else "After price increase"
    )
    return daily_sales


daily_sales = load_daily_sales()
average_sales = ( daily_sales.groupby("Period", as_index=False)["Sales"].mean().round({"Sales": 2}) )
before_average = average_sales.loc[average_sales["Period"] == "Before price increase", "Sales"].iat[0]
after_average = average_sales.loc[average_sales["Period"] == "After price increase", "Sales"].iat[0]

figure = px.line(
    daily_sales,
    x="Date",
    y="Sales",
    color="Period",
    color_discrete_map={ "Before price increase": "#7a3e00", "After price increase": "#ff4f7b" },
    labels={"Date": "Date", "Sales": "Total sales ($)", "Period": ""},
    title="Pink Morsel daily sales",
)

figure.update_traces(line={"width": 3})
figure.update_layout(
    plot_bgcolor="#fffaf5",
    paper_bgcolor="#fffaf5",
    hovermode="x unified",
    legend={"orientation": "h", "y": 1.08, "x": 0},
    margin={"l": 40, "r": 20, "t": 80, "b": 40},
)
figure.update_xaxes(showgrid=False)
figure.update_yaxes(gridcolor="#f0d8c2")
figure.add_shape(
    type="line",
    x0=PRICE_INCREASE_DATE,
    x1=PRICE_INCREASE_DATE,
    y0=0,
    y1=1,
    xref="x",
    yref="paper",
    line={"dash": "dash", "color": "#1f2937", "width": 2},
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
    bgcolor="#fffaf5",
)

app = Dash(__name__)
app.title = "Soul Foods Sales Visualiser"

app.layout = html.Div(
    [
        html.H1("Soul Foods Pink Morsel Sales Visualiser"),
        html.P(
            "Daily Pink Morsel sales jump after the 15 January 2021 price increase."
        ),
        html.P(
            (
                f"Average daily sales before the increase: ${before_average:,.2f}. "
                f"Average daily sales after the increase: ${after_average:,.2f}."
            )
        ),
        dcc.Graph(figure=figure),
    ],
    style={
        "padding": "32px 20px",
        "fontFamily": "Arial, sans-serif",
        "backgroundColor": "#fffaf5",
        "color": "#2b2118",
    },
)


if __name__ == "__main__":
    app.run(debug=True)