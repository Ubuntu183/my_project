from dash import html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
from data import df, count_grouped, region_list

layout = dbc.Container([
    dbc.Row ([
        dbc.Col(
            html.Div([
                html.H1("Общая статистика"),
                html.Hr(style={'color': 'black'})
            ], style={'textAlign': 'center'})
        )
    ]),

    html.Br(),
    
        dbc.Row([
            dbc.Col([
                dcc.Graph(
                    id='sales-line-chart',
                    figure={
                        'data': [
                            {'x': count_grouped['Year'], 'y': count_grouped['Count'], 'type': 'line', 'name': 'Продажи'},
                        ],
                        'layout': {
                            'title': 'Кол-во выпущенных игр по годам',
                            'xaxis': {'title': 'Год'},
                            'yaxis': {'title': 'Кол-во игр'},
                            'margin': {'l': 80, 'r': 80, 't': 20, 'b': 40},
                            'height': 350
                        }
                    }
                )
            ])
        ]),

    html.Br(),

        dbc.Row([
            dbc.Col([
                html.P("Регион:")
            ],width=1),
            dbc.Col([
                dcc.Dropdown(
                    id = 'crossfilter-reg',
                    options = [{'label': i, 'value': j} for i,j in region_list],
                    value = region_list[0][1],
                    multi = False,
                    clearable=False
                )
            ],width=2),
            dbc.Col([
                html.P("Год:")
            ],width=1),
            dbc.Col([
                dcc.Slider(
                id = 'crossfilter-year',
                min = df['Year'].min(),
                max = df['Year'].max(),
                value = 2009,
                step = 1,
                marks = {str(year):
                    str(year) for year in range(int(df['Year'].min()), int(df['Year'].max()), 5)},
                tooltip = {"placement": "bottom", "always_visible": False}),
            ],width=7),
        ], justify='center', style={'textAlign': 'center'}),

    html.Br(),

    dbc.Container([
        dbc.Row ([
            dbc.Col([
                dbc.Row([
                    html.H5("Топ 5 жанров"),
                    html.Div(id="table1"),
                ], style={'textAlign': 'center'})
            ],width=4, className='mx-5'),
            dbc.Col([
                dbc.Row([
                    html.H5("Топ 5 платформ"),
                    html.Div(id="table2"),
                ], style={'textAlign': 'center'})
            ],width=4, className='mx-5')
        ], justify='center', style={'textAlign': 'center'}),
        ], style={'textAlign': 'center'}),
])

@callback(
    [Output('table1', 'children'),
    Output('table2', 'children'),
    ],
    [Input('crossfilter-reg', 'value'),
    Input('crossfilter-year', 'value'),
    ]
)
def update_card(region, year):
    df_year=df[df['Year'] == year]
    
    genre_grouped = df_year.groupby('Genre')[region].sum().reset_index().sort_values(by=region, ascending=False)
    platform_grouped = df_year.groupby('Platform')[region].sum().reset_index().sort_values(by=region, ascending=False)

    genre_grouped[region] = genre_grouped[region].round(2)
    platform_grouped[region] = platform_grouped[region].round(2)

    genre_table=genre_grouped.iloc[0:5][['Genre', region]]
    platform_table=platform_grouped.iloc[0:5][['Platform', region]]

    genre_table.rename(columns={'Genre': 'Название жанра', region: 'Продажи  млн. $'}, inplace=True)
    platform_table.rename(columns={'Platform': 'Название платформы', region: 'Продажи  млн. $'}, inplace=True)

    table1 = dbc.Table.from_dataframe(
        genre_table, striped=True, bordered=True, hover=True, index=False)
    
    table2 = dbc.Table.from_dataframe(
        platform_table, striped=True, bordered=True, hover=True, index=False)

    return table1, table2