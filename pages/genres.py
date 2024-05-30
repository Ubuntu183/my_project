from dash import html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
from data import df, genre_list

layout = dbc.Container([
    dbc.Row ([
        dbc.Col(
            html.Div([
                html.H1("Платформы"),
                html.Hr(style={'color': 'black'})
            ], style={'textAlign': 'center'})
        )
    ]),

    html.Br(),

    dbc.Row([
            dbc.Col([
                html.P("Жанр:")
            ],width=1),
            dbc.Col([
                dcc.Dropdown(
                    id = 'crossfilter-genre',
                    options = [{'label': i, 'value': i} for i in genre_list],
                    value = genre_list[1],
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
            ],width=8),
        ]),

    html.Br(),

    dbc.Container([
        dbc.Row ([
            dbc.Col([
                 dbc.Card([
                    dbc.Row([
                        dbc.CardHeader("Количество игр", style={'width': '90%'})
                    ], justify="center"),
                    dbc.Row([
                        dbc.Col([
                            dbc.CardImg(src='/static/images/games.png')], width= 4),
                        dbc.Col([
                            dbc.CardBody(
                                html.P(
                                id='genre_card_text1',
                                className="card-value"),
                            )], width= 8),
                    ], style={"height": "10vh"})
                ], color = "primary", outline=True, style={'textAlign': 'center'}),
            ],width=3),
            dbc.Col([
                 dbc.Card([
                    dbc.Row([
                        dbc.CardHeader("Продажи за всё время", style={'width': '90%'})
                    ], justify="center"),
                    dbc.Row([
                        dbc.Col([
                            dbc.CardImg(src='/static/images/wallet.png')], width= 4),
                        dbc.Col([
                            dbc.CardBody(
                                html.P(
                                id='genre_card_text2',
                                className="card-value"),
                            )], width= 8),
                    ], style={"height": "10vh"})
                ], color = "primary", outline=True, style={'textAlign': 'center'}),
            ],width=3),
            dbc.Col([
                 dbc.Card([
                    dbc.Row([
                        dbc.CardHeader("Самая популярная игра", style={'width': '90%'})
                    ], justify="center"),
                    dbc.Row([
                        dbc.Col([
                            dbc.CardImg(src='/static/images/globe.png')], width= 4),
                        dbc.Col([
                            dbc.CardBody(
                                html.P(
                                id='genre_card_text3',
                                className="card-value"),
                            )], width= 8),
                    ], style={"height": "10vh"})
                ], color = "primary", outline=True, style={'textAlign': 'center'}),
            ],width=3),
        ], justify='center', style={'textAlign': 'center'}),
    ], style={'textAlign': 'center'}),

    html.Br(),

    dbc.Container([
        dbc.Row ([
            dbc.Col([
                dbc.Row([
                    html.H5("Топ игр жанра", style={'margin-bottom': '15px',}),
                    html.Div(id="genre_top_games_table"),
                ], style={'textAlign': 'center'})
            ],width=6, className='mx-1'),
            dbc.Col([
                dbc.Row([
                    html.H5("Распределение игр по платформам"),
                    dcc.Graph(id = 'genre_platform_pie'),
                ], style={'textAlign': 'center'})
            ],width=5, className='mx-1')
        ]),
        ], style={'textAlign': 'center'}),
])

@callback(
    [Output('genre_card_text1','children'),
    Output('genre_card_text2','children'),
    Output('genre_card_text3','children'),
    Output('genre_top_games_table', 'children'),
    Output('genre_platform_pie', 'figure'),
    ],
    [Input('crossfilter-genre', 'value'),
    Input('crossfilter-year', 'value'),
    ]

)
def update_all(genre, year):
    df_genre=df[(df['Genre'] == genre)&(df['Year'] == year)]
    genre_games = df_genre.groupby('Name')['Global_Sales'].sum().reset_index().sort_values(by='Global_Sales', ascending=False)
    genre_games['Global_Sales'] = genre_games['Global_Sales'].round(2)

    ct1=str(len(df_genre)) + " шт."
    ct2=str(df_genre['Global_Sales'].sum().round(2)) + " млн. $"
    ct3=str(df_genre['Name'].iloc[0])

    t = genre_games.iloc[0:8][['Name', 'Global_Sales']]
    t.rename(columns={'Name': 'Название', 'Global_Sales': 'Продажи, млн. $'}, inplace=True)

    top_games_table_g = dbc.Table.from_dataframe(
        t, striped=True, bordered=True, hover=True, index=False)
    
    platform_counts = df_genre['Platform'].value_counts().reset_index()
    platform_counts.columns = ['Platform', 'Count']

    figure = px.pie(platform_counts, values='Count', names='Platform', height=500, width=650)
    figure.update_layout(margin=dict(t=15))

    return ct1, ct2, ct3, top_games_table_g, figure