from dash import Dash, html, dcc, callback, Input, Output
import plotly.express as px
import pandas as pd
import requests as re


def zajecia(df):
    fig = px.bar(
        df,
        x="godzinaOd",
        y="liczba_zajec",
        template="plotly_white",
    )

    fig.update_layout(
        xaxis_title=None,
        yaxis_title=None,
        showlegend=False,
        height=350,
        margin=dict(l=20, r=20, t=20, b=20),
    )
    return fig


def karta(id_wartosci, tytul, value=0):
    return html.Div(
        children=[
            html.Div(
                id=id_wartosci,
                children=value,
                style={
                    "fontSize": "44px",
                    "fontWeight": "bold",
                    "textAlign": "center",
                    "lineHeight": "1"
                }
            ),
            html.Div(
                children=tytul,
                style={
                    "fontSize": "16px",
                    "fontWeight": "bold",
                    "textAlign": "center",
                    "marginTop": "8px"
                }
            )
        ],
        style={
            "border": "1px solid black",
            "width": "180px",
            "height": "105px",
            "display": "flex",
            "flexDirection": "column",
            "justifyContent": "center",
            "alignItems": "center",
            "backgroundColor": "white"
        }
    )


r = re.request(method="GET", url="http://127.0.0.1:8000/classes")

data = r.json()
df = pd.DataFrame(data)

app = Dash()
data_zajec = df["Data"].unique()
godzina_od = df["godzinaOd"].unique()
godzina_do = df["godzinaDo"].unique()
prowadzacy = df["prowadzacy"].unique()
nazwaSali = df["nazwaSali"].unique()
budynekNazwa = df["budynekNazwa"].unique()

liczba_zajec_po_godzinie = (
    df.groupby("godzinaOd")
      .size()
      .reset_index(name="liczba_zajec")
      .sort_values("godzinaOd")
)

fig = zajecia(liczba_zajec_po_godzinie)

app.layout = html.Div(children=[
    html.Div(
        children=[
            dcc.Dropdown(
                data_zajec,
                data_zajec[0],
                id="data-dropdown",
                style={"flex": "1"}
            ),
            dcc.Dropdown(
                godzina_od,
                id="godzina-od-dropdown",
                style={"flex": "1"},
                placeholder="Wybierz godzinę rozpoczęcia zajęć"
            ),
            dcc.Dropdown(
                godzina_do,
                id="godzina-do-dropdown",
                style={"flex": "1"},
                placeholder="Wybierz godzinę zakończenia zajęć"
            )
        ],
        style={
            "display": "flex",
            "gap": "5px",
            "width": "100%"
        }
    ),
    html.Div(
        children=[
            dcc.Dropdown(
                budynekNazwa,
                "Dąbrowa",
                id="budynekNazwa-dropdown",
                style={"flex": "1"}
            ),
            dcc.Dropdown(
                prowadzacy,
                id="prowadzacy-dropdown",
                style={"flex": "1"},
                placeholder="Wybierz prowadzącego"
            ),
            dcc.Dropdown(
                nazwaSali,
                id="nazwaSali-dropdown",
                style={"flex": "1"},
                placeholder="Wybierz salę"
            )
        ],
        style={
            "marginTop": "5px",
            "display": "flex",
            "gap": "5px",
            "width": "100%"
        }
    ),
    html.Div(
        children=[
            dcc.Graph(
                id='example-graph',
                figure=fig
            ),
            karta("liczba-zajec-card", "Liczba zajęć")
        ],
        style={
            "marginTop": "5px",
            "display": "flex",
            "gap": "5px",
            "width": "100%"
        }
    ),

]
)


@callback(
    Output("example-graph", "figure"),
    Input("data-dropdown", "value")
)
def update_output_data(value):
    dff = df[df.Data == value]
    liczba_zajec_po_godzinie = (
        dff.groupby("godzinaOd")
        .size()
        .reset_index(name="liczba_zajec")
        .sort_values("godzinaOd")
    )
    fig = zajecia(liczba_zajec_po_godzinie)
    return fig


@callback(
    Output("liczba-zajec-card", "children"),
    Input("data-dropdown", "value")
)
def update_count_data(value):
    dff = df[df.Data == value]
    card = karta("liczba-zajec-card", "Liczba zajęć", len(dff))
    return card


def run_app():
    if __name__ == '__main__':
        app.run(debug=True)


run_app()

# print(df["Data"])
