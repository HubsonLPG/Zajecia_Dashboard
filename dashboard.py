import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import requests as re
from dash import Dash, Input, Output, callback, dash_table, dcc, html


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
        margin={"l": 20, "r": 20, "t": 20, "b": 20},
    )
    return fig


def karta(id_wartosci, tytul, value=0):
    return html.Div(
        children=[
            html.Div(
                id=id_wartosci,
                children=value,
                style={
                    "fontSize": "46px",
                    "fontWeight": "700",
                    "textAlign": "center",
                    "lineHeight": "1",
                    "marginBottom": "10px"
                }
            ),
            html.Div(
                children=tytul,
                style={
                    "fontSize": "20px",
                    "fontWeight": "700",
                    "textAlign": "center",
                    "lineHeight": "1.2"
                }
            )
        ],
        style={
            "border": "1px solid black",
            "width": "260px",
            "height": "150px",
            "boxSizing": "border-box",
            "display": "flex",
            "flexDirection": "column",
            "justifyContent": "center",
            "alignItems": "center",
            "backgroundColor": "white",
            "overflow": "hidden",
            # "marginTop": "90px",
            # "marginLeft": "60px"
        }
    )


r = re.request(method="GET", url="http://127.0.0.1:8000/classes")

data = r.json()
df = pd.DataFrame(data)

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME])
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
    # dbc.Container(
    #     dbc.Alert("Hello Bootstrap!", color="success"),
    #     className="p-5",
    # ),
    html.Div(
        children=[
            dcc.Dropdown(
                data_zajec,
                # data_zajec[0],
                id="data-dropdown",
                style={"flex": "1"},
                placeholder="Wybierz datę"
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
            "marginTop": "5px",
            "marginLeft": "5px",
            "marginRight": "5px",
            "display": "flex",
            "gap": "5px",
            "width": "calc(100% - 10px)"
        }
    ),
    html.Div(
        children=[
            dcc.Dropdown(
                budynekNazwa,
                id="budynekNazwa-dropdown",
                style={"flex": "1"},
                placeholder="Wybierz budynek"
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
            "marginLeft": "5px",
            "marginRight": "5px",
            "display": "flex",
            "gap": "5px",
            "width": "calc(100% - 10px)"
        }
    ),
    html.Div(
        children=[
            html.Div(
                children=[
                    dcc.Graph(
                        id='example-graph',
                        figure=fig
                    ),
                    html.Div(
                        children=[
                            karta("liczba-zajec-card", "Liczba zajęć")
                        ],
                        style={
                            # "marginTop": "5px",
                            # "marginLeft": "5px",
                            "margin": "15px auto"
                        }
                    )
                ],
                style={
                    "marginTop": "5px",
                    "marginLeft": "5px",
                    "marginRight": "5px",
                    "display": "flex",
                    "gap": "5px",
                    # "width": "70%",
                    "border": "1px solid black",
                    "backgroundColor": "white",
                    "alignItems": "center"
                }

            ),
            # html.Div(
            #     children=[
            #         karta("liczba-zajec-card", "Liczba zajęć")
            #     ],
            #     style={
            #         "marginTop": "5px",
            #         "marginLeft": "5px"
            #     }
            # )
        ]
    ),
    html.Div(
        children=[
            dash_table.DataTable(
                id="classes-table",
                columns=[
                    {"name": "Data", "id": "Data"},
                    {"name": "Godzina od", "id": "godzinaOd"},
                    {"name": "Godzina do", "id": "godzinaDo"},
                    {"name": "Prowadzący", "id": "prowadzacy"},
                    {"name": "Sala", "id": "nazwaSali"},
                    {"name": "Budynek", "id": "budynekNazwa"},
                ],
                data=df[
                    [
                        "Data",
                        "godzinaOd",
                        "godzinaDo",
                        "prowadzacy",
                        "nazwaSali",
                        "budynekNazwa",
                    ]
                ].to_dict("records"),  # pyright: ignore[reportArgumentType]

                page_action="native",
                page_size=15,

                sort_action="native",
                filter_action="native",

                style_table={
                    "overflowX": "auto",
                },

                style_cell={
                    "textAlign": "left",
                    "padding": "8px",
                },

                style_header={
                    "fontWeight": "bold",
                    "textAlign": "center",
                },
            )
        ],
        style={
            "marginTop": "5px",
            "marginLeft": "5px",
            "marginRight": "5px",
            "border": "1px solid black",
            "backgroundColor": "white",
        }
    ),
],
    style={
    "width": "calc(100% - 30px)",
    "maxWidth": "1400px",
    "margin": "15px auto",
}
)


def filtruj(
    data_value=None,
    godzina_od_value=None,
    godzina_do_value=None,
    budynek_value=None,
    prowadzacy_value=None,
    sala_value=None
):
    dff = df.copy()

    if data_value:
        dff = dff[dff["Data"] == data_value]

    if godzina_od_value:
        dff = dff[dff["godzinaOd"] == godzina_od_value]

    if godzina_do_value:
        dff = dff[dff["godzinaDo"] == godzina_do_value]

    if budynek_value:
        dff = dff[dff["budynekNazwa"] == budynek_value]

    if prowadzacy_value:
        dff = dff[dff["prowadzacy"] == prowadzacy_value]

    if sala_value:
        dff = dff[dff["nazwaSali"] == sala_value]

    return dff


@callback(
    Output("example-graph", "figure"),
    Output("classes-table", "data"),
    Output("liczba-zajec-card", "children"),

    Output("data-dropdown", "options"),
    Output("godzina-od-dropdown", "options"),
    Output("godzina-do-dropdown", "options"),
    Output("budynekNazwa-dropdown", "options"),
    Output("prowadzacy-dropdown", "options"),
    Output("nazwaSali-dropdown", "options"),

    Input("data-dropdown", "value"),
    Input("godzina-od-dropdown", "value"),
    Input("godzina-do-dropdown", "value"),
    Input("budynekNazwa-dropdown", "value"),
    Input("prowadzacy-dropdown", "value"),
    Input("nazwaSali-dropdown", "value"),
)
def update_dashboard(
    data_value,
    godzina_od_value,
    godzina_do_value,
    budynek_value,
    prowadzacy_value,
    sala_value
):
    # =========================
    # FILTROWANIE GŁÓWNE
    # =========================

    dff = filtruj(
        data_value,
        godzina_od_value,
        godzina_do_value,
        budynek_value,
        prowadzacy_value,
        sala_value
    )

    # =========================
    # WYKRES
    # =========================

    liczba_zajec_po_godzinie = (
        dff.groupby("godzinaOd")
        .size()
        .reset_index(name="liczba_zajec")
        .sort_values("godzinaOd")
    )

    fig = zajecia(liczba_zajec_po_godzinie)

    # =========================
    # TABELA
    # =========================

    table_data = dff[
        [
            "Data",
            "godzinaOd",
            "godzinaDo",
            "prowadzacy",
            "nazwaSali",
            "budynekNazwa",
        ]
    ].to_dict("records")

    # =========================
    # OPCJE DROPDOWNÓW
    # każdy dropdown filtrujemy
    # wszystkimi pozostałymi
    # =========================

    data_options = (
        filtruj(
            None,
            godzina_od_value,
            godzina_do_value,
            budynek_value,
            prowadzacy_value,
            sala_value
        )["Data"]
        .dropna()
        .unique()
        .tolist()
    )

    godzina_od_options = (
        filtruj(
            data_value,
            None,
            godzina_do_value,
            budynek_value,
            prowadzacy_value,
            sala_value
        )["godzinaOd"]
        .dropna()
        .unique()
        .tolist()
    )

    godzina_do_options = (
        filtruj(
            data_value,
            godzina_od_value,
            None,
            budynek_value,
            prowadzacy_value,
            sala_value
        )["godzinaDo"]
        .dropna()
        .unique()
        .tolist()
    )

    budynek_options = (
        filtruj(
            data_value,
            godzina_od_value,
            godzina_do_value,
            None,
            prowadzacy_value,
            sala_value
        )["budynekNazwa"]
        .dropna()
        .unique()
        .tolist()
    )

    prowadzacy_options = (
        filtruj(
            data_value,
            godzina_od_value,
            godzina_do_value,
            budynek_value,
            None,
            sala_value
        )["prowadzacy"]
        .dropna()
        .unique()
        .tolist()
    )

    sala_options = (
        filtruj(
            data_value,
            godzina_od_value,
            godzina_do_value,
            budynek_value,
            prowadzacy_value,
            None
        )["nazwaSali"]
        .dropna()
        .unique()
        .tolist()
    )

    # =========================
    # RETURN
    # =========================

    return (
        fig,
        table_data,
        len(dff),

        data_options,
        godzina_od_options,
        godzina_do_options,
        budynek_options,
        prowadzacy_options,
        sala_options
    )


def run_app():
    if __name__ == '__main__':
        app.run(
            host="0.0.0.0",
            port=8050,
            debug=True
        )


run_app()
