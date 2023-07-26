import dash
from dash import dcc
from dash import html
import pandas as pd
import plotly.express as px
import numpy as np
import openpyxl as op
from dash import Output, Input


s = pd.read_excel('1.xlsx', sheet_name='Лист1')# читаем файл
s.to_csv("./data.csv", sep=",")
s['Дата'] = pd.to_datetime(s['Дата'], format="%Y-%m-%d")
# делим таблицу по фикс и флоат
s_fix = s.loc[s['Тип'] == 'ФИКС']
s_float = s.loc[s['Тип'] == 'ФЛОАТ']
s_float = s_float.reset_index(drop=True)


external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
        "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    }]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.H1(children="Тестовое задание", className="header-title"),
                html.P(
                    children="Динамика ставок БКД", className="header-description"
                )
            ],
            className='header'
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Период", className="menu-title"),
                        dcc.Dropdown(
                            id="period-filter",
                            options=[
                                {"label": period, "value": period}
                                for period in s_fix.columns[2:]
                            ],
                            value=s_fix.columns[5],
                            clearable=False,
                            searchable=False,
                            className="dropdown",
                        ),
                    ],
                ),
                html.Div(
                    children=[
                        html.Div(
                            children="Дата",
                            className="menu-title"
                            ),
                        dcc.DatePickerRange(
                            id="date-range",
                            min_date_allowed=s_fix.Дата.min().date(),
                            max_date_allowed=s_fix.Дата.max().date(),
                            start_date=s_fix.Дата.min().date(),
                            end_date=s_fix.Дата.max().date(),
                            className="dropdown"
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(children="Ставка ЦБ", className="menu-title"),
                        dcc.Input(
                            id="cb_input",
                            type="number",
                            value=7.5,
                            className="dropdown"
                        )
                    ],
                ),
            ],
            className="menu",
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="graph", config={"displayModeBar": True},
                    ),
                    className="card",
                )
            ],
            className="wrapper",
        ),
    ]
)

@app.callback(
    [dash.dependencies.Output('graph', "figure")],
    [
        dash.dependencies.Input("period-filter", "value"),
        dash.dependencies.Input("date-range", "start_date"),
        dash.dependencies.Input("date-range", "end_date"),
        dash.dependencies.Input("cb_input", "value"),
    ]
)

def update_charts(period, start_date, end_date, cb_value):
    mask = (
         (s_fix.Дата >= start_date)
        & (s_fix.Дата <= end_date)
    )
    filtered_data = s_fix.loc[mask,:]
    figure = {
        "data": [
                    {
                        "x": filtered_data['Дата'],
                        "y": s_fix[period]*100,
                        "type": "lines",
                        'name' : 'ФИКС',
                        'text' : round(s_fix[period]*100, 2),
                        'textposition': 'top_right',
                        'mode' : 'markers+lines+text',
                    },
                    {
                        "x": filtered_data["Дата"],
                        "y": s_float[period]*100+cb_value,
                        "type": "lines", 'name' : 'ФЛОАТ',
                        'text' : round(s_float[period]*100+cb_value, 2),
                        'textposition' : 'top_right',
                        'mode': 'markers+lines+text',
                    }
                ],
                'layout':{
                    'title':f"Динамика ставок БКД за период {period} в промежутке {start_date}:{end_date}",
                    'xaxis':{
                        'title':'Временной промежуток'
                    },
                    'yaxis':{
                        'title':'Данные в %'
                    }
                }
    }
    return [figure]

#
if __name__ == "__main__":
    app.run_server(debug=True,
                   host = '127.0.0.1')