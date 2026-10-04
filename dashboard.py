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
                    "fontSize": "42px",
                    "fontWeight": "700",
                    "lineHeight": "1",
                    "marginBottom": "8px"
                }
            ),
            html.Div(
                tytul,
                style={
                    "fontSize": "16px",
                    "fontWeight": "600",
                    "color": "#6b7280"
                }
            )
        ],
        style={
            "width": "220px",
            "height": "130px",
            "display": "flex",
            "flexDirection": "column",
            "justifyContent": "center",
            "alignItems": "center",
            "backgroundColor": "white",
            "border": "1px solid #e5e7eb",
            "borderRadius": "12px",
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

app.layout = html.Div(
    children=[
        # =====================================================
        # STORE + AUTO REFRESH
        # =====================================================

        dcc.Store(
            id="data-store",
            data=df.to_dict("records")
        ),

        dcc.Interval(
            id="refresh-interval",
            interval=60 * 1000,
            n_intervals=0
        ),

        # =====================================================
        # GŁÓWNY KONTENER
        # =====================================================

        html.Div(
            children=[

                # =====================================================
                # NAGŁÓWEK
                # =====================================================

                html.Div(
                    children=[
                        html.Div(
                            children=[
                                html.H2(
                                    "Dashboard zajęć",
                                    style={
                                        "margin": "0",
                                        "fontSize": "28px",
                                        "fontWeight": "700",
                                        "color": "#111827",
                                    }
                                ),

                                # html.Div(
                                #     "Podgląd i filtrowanie aktualnych zajęć",
                                #     style={
                                #         "marginTop": "4px",
                                #         "fontSize": "14px",
                                #         "color": "#6b7280",
                                #     }
                                # )
                            ]
                        ),

                        html.Div(
                            children=[
                                html.I(
                                    className="fa-solid fa-rotate",
                                    style={
                                        "marginRight": "7px"
                                    }
                                ),

                                html.Span(
                                    "Dane odświeżane co 60 sekund"
                                )
                            ],
                            style={
                                "fontSize": "13px",
                                "color": "#6b7280",
                                "display": "flex",
                                "alignItems": "center",
                            }
                        )
                    ],

                    style={
                        "display": "flex",
                        "justifyContent": "space-between",
                        "alignItems": "center",
                        "marginBottom": "18px",
                        "gap": "20px",
                        "flexWrap": "wrap",
                    }
                ),

                # =====================================================
                # FILTRY
                # =====================================================

                html.Div(
                    children=[
                        html.Div(
                            "Filtry",
                            style={
                                "fontSize": "16px",
                                "fontWeight": "700",
                                "color": "#374151",
                                "marginBottom": "12px",
                            }
                        ),

                        # Pierwszy rząd
                        html.Div(
                            children=[
                                html.Div(
                                    children=[
                                        html.Div(
                                            "Data",
                                            style={
                                                "fontSize": "12px",
                                                "fontWeight": "600",
                                                "color": "#6b7280",
                                                "marginBottom": "5px",
                                            }
                                        ),

                                        dcc.Dropdown(
                                            data_zajec,
                                            data_zajec[0],
                                            id="data-dropdown",
                                            clearable=True,
                                        )
                                    ],
                                    style={
                                        "flex": "1",
                                        "minWidth": "220px",
                                    }
                                ),

                                html.Div(
                                    children=[
                                        html.Div(
                                            "Godzina rozpoczęcia",
                                            style={
                                                "fontSize": "12px",
                                                "fontWeight": "600",
                                                "color": "#6b7280",
                                                "marginBottom": "5px",
                                            }
                                        ),

                                        dcc.Dropdown(
                                            godzina_od,
                                            id="godzina-od-dropdown",
                                            placeholder="Wybierz godzinę"
                                        )
                                    ],
                                    style={
                                        "flex": "1",
                                        "minWidth": "220px",
                                    }
                                ),

                                html.Div(
                                    children=[
                                        html.Div(
                                            "Godzina zakończenia",
                                            style={
                                                "fontSize": "12px",
                                                "fontWeight": "600",
                                                "color": "#6b7280",
                                                "marginBottom": "5px",
                                            }
                                        ),

                                        dcc.Dropdown(
                                            godzina_do,
                                            id="godzina-do-dropdown",
                                            placeholder="Wybierz godzinę"
                                        )
                                    ],
                                    style={
                                        "flex": "1",
                                        "minWidth": "220px",
                                    }
                                ),
                            ],

                            style={
                                "display": "flex",
                                "gap": "12px",
                                "flexWrap": "wrap",
                                "marginBottom": "12px",
                            }
                        ),

                        # Drugi rząd
                        html.Div(
                            children=[
                                html.Div(
                                    children=[
                                        html.Div(
                                            "Budynek",
                                            style={
                                                "fontSize": "12px",
                                                "fontWeight": "600",
                                                "color": "#6b7280",
                                                "marginBottom": "5px",
                                            }
                                        ),

                                        dcc.Dropdown(
                                            budynekNazwa,
                                            id="budynekNazwa-dropdown",
                                            placeholder="Wybierz budynek"
                                        )
                                    ],
                                    style={
                                        "flex": "1",
                                        "minWidth": "220px",
                                    }
                                ),

                                html.Div(
                                    children=[
                                        html.Div(
                                            "Prowadzący",
                                            style={
                                                "fontSize": "12px",
                                                "fontWeight": "600",
                                                "color": "#6b7280",
                                                "marginBottom": "5px",
                                            }
                                        ),

                                        dcc.Dropdown(
                                            prowadzacy,
                                            id="prowadzacy-dropdown",
                                            placeholder="Wybierz prowadzącego"
                                        )
                                    ],
                                    style={
                                        "flex": "1",
                                        "minWidth": "220px",
                                    }
                                ),

                                html.Div(
                                    children=[
                                        html.Div(
                                            "Sala",
                                            style={
                                                "fontSize": "12px",
                                                "fontWeight": "600",
                                                "color": "#6b7280",
                                                "marginBottom": "5px",
                                            }
                                        ),

                                        dcc.Dropdown(
                                            nazwaSali,
                                            id="nazwaSali-dropdown",
                                            placeholder="Wybierz salę"
                                        )
                                    ],
                                    style={
                                        "flex": "1",
                                        "minWidth": "220px",
                                    }
                                ),
                            ],

                            style={
                                "display": "flex",
                                "gap": "12px",
                                "flexWrap": "wrap",
                            }
                        ),
                    ],

                    style={
                        "backgroundColor": "white",
                        "border": "1px solid #e5e7eb",
                        "borderRadius": "12px",
                        "padding": "18px",
                        "marginBottom": "14px",
                        "boxShadow": "0 1px 3px rgba(0,0,0,0.05)",
                    }
                ),

                # =====================================================
                # WYKRES + KPI
                # =====================================================

                html.Div(
                    children=[
                        # Wykres
                        html.Div(
                            children=[
                                html.Div(
                                    "Liczba zajęć według godziny rozpoczęcia",
                                    style={
                                        "fontSize": "16px",
                                        "fontWeight": "700",
                                        "color": "#374151",
                                        "marginBottom": "5px",
                                    }
                                ),

                                dcc.Graph(
                                    id="example-graph",
                                    figure=fig,
                                    config={
                                        "displayModeBar": False
                                    },
                                    style={
                                        "width": "100%",
                                    }
                                )
                            ],

                            style={
                                "flex": "1",
                                "minWidth": "500px",
                            }
                        ),

                        # KPI
                        html.Div(
                            children=[
                                karta(
                                    "liczba-zajec-card",
                                    "Liczba zajęć"
                                )
                            ],

                            style={
                                "minWidth": "260px",
                                "display": "flex",
                                "justifyContent": "center",
                                "alignItems": "center",
                            }
                        )
                    ],

                    style={
                        "display": "flex",
                        "gap": "20px",
                        "alignItems": "center",
                        "flexWrap": "wrap",

                        "backgroundColor": "white",
                        "border": "1px solid #e5e7eb",
                        "borderRadius": "12px",
                        "padding": "18px",

                        "marginBottom": "14px",

                        "boxShadow": "0 1px 3px rgba(0,0,0,0.05)",
                    }
                ),

                # =====================================================
                # TABELA
                # =====================================================

                html.Div(
                    children=[
                        html.Div(
                            children=[
                                html.Div(
                                    "Szczegóły zajęć",
                                    style={
                                        "fontSize": "16px",
                                        "fontWeight": "700",
                                        "color": "#374151",
                                    }
                                ),

                                html.Div(
                                    "Tabela uwzględnia aktywne filtry",
                                    style={
                                        "fontSize": "13px",
                                        "color": "#9ca3af",
                                        "marginTop": "3px",
                                    }
                                )
                            ],

                            style={
                                "marginBottom": "14px"
                            }
                        ),

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
                            ].to_dict("records"),  # type: ignore

                            page_action="native",
                            page_size=10,

                            sort_action="native",
                            filter_action="native",

                            style_table={
                                "overflowX": "auto",
                                "border": "1px solid #e5e7eb",
                                "borderRadius": "8px",
                            },

                            style_header={
                                "backgroundColor": "#f9fafb",
                                "color": "#374151",
                                "fontWeight": "700",
                                "textAlign": "center",
                                "border": "none",
                                "borderBottom": "1px solid #d1d5db",
                                "padding": "12px",
                            },

                            style_filter={
                                "backgroundColor": "#ffffff",
                                "border": "none",
                                "borderBottom": "1px solid #e5e7eb",
                            },

                            style_cell={
                                "padding": "10px",
                                "textAlign": "left",
                                "border": "none",
                                "borderBottom": "1px solid #e5e7eb",
                                "fontSize": "14px",
                                "fontFamily": "Arial, sans-serif",
                                "whiteSpace": "normal",
                                "height": "auto",
                            },

                            style_data_conditional=[
                                {
                                    "if": {
                                        "row_index": "odd"
                                    },
                                    "backgroundColor": "#fafafa",
                                },

                                {
                                    "if": {
                                        "state": "selected"
                                    },
                                    "backgroundColor": "#e8f0fe",
                                    "border": "1px solid #9bbcff",
                                }
                            ],  # type: ignore
                        )
                    ],

                    style={
                        "backgroundColor": "white",
                        "border": "1px solid #e5e7eb",
                        "borderRadius": "12px",
                        "padding": "18px",

                        "boxShadow": "0 1px 3px rgba(0,0,0,0.05)",
                    }
                )
            ],

            style={
                "width": "calc(100% - 30px)",
                "maxWidth": "1400px",
                "margin": "0 auto",
                "padding": "22px 0",
            }
        )
    ],

    style={
        "minHeight": "100vh",
        "backgroundColor": "#f3f4f6",
        "fontFamily": "Arial, sans-serif",
    }
)


@callback(
    Output("data-store", "data"),
    Input("refresh-interval", "n_intervals")
)
def refresh_data(n):
    r = re.get("http://127.0.0.1:8000/classes")
    r.raise_for_status()

    data = r.json()

    return data


def filtruj(
    df,
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

    Input("data-store", "data"),
    Input("data-dropdown", "value"),
    Input("godzina-od-dropdown", "value"),
    Input("godzina-do-dropdown", "value"),
    Input("budynekNazwa-dropdown", "value"),
    Input("prowadzacy-dropdown", "value"),
    Input("nazwaSali-dropdown", "value"),
)
def update_dashboard(
    stored_data,
    data_value,
    godzina_od_value,
    godzina_do_value,
    budynek_value,
    prowadzacy_value,
    sala_value
):
    df = pd.DataFrame(stored_data)
    # =========================
    # FILTROWANIE GŁÓWNE
    # =========================

    dff = filtruj(
        df,
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
            df,
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
            df,
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
            df,
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
            df,
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
            df,
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
            df,
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
            debug=False
        )


run_app()
