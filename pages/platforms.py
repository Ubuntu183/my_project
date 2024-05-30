from dash import html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
from data import df, platforms_list

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
            html.P("Платформа:")
        ],width=1),
        dbc.Col([
            dcc.Dropdown(
                id = 'crossfilter-platform',
                options = [{'label': i, 'value': i} for i in platforms_list],
                value = platforms_list[1],
                multi = False,
                clearable=False
            )
        ],width=3),
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
                                id='platform_card_text1',
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
                                id='platform_card_text2',
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
                                id='platform_card_text3',
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
                    html.H5("Топ игр на платформе", style={'margin-bottom': '15px',}),
                    html.Div(id="platform_top_games_table"),
                ], style={'textAlign': 'center'})
            ],width=6, className='mx-1'),
            dbc.Col([
                dbc.Row([
                    html.H5("Распределение игр платформы по жанрам"),
                    dcc.Graph(id = 'platform_genre_pie'),
                ], style={'textAlign': 'center'})
            ],width=5, className='mx-1')
        ]),
        ], style={'textAlign': 'center'}),
])

@callback(
    [Output('platform_card_text1','children'),
    Output('platform_card_text2','children'),
    Output('platform_card_text3','children'),
    Output('platform_top_games_table', 'children'),
    Output('platform_genre_pie', 'figure'),
    ],
    Input('crossfilter-platform', 'value'),

)
def update_all(platform):
    df_platform=df[df['Platform'] == platform]
    popular_games = df_platform.sort_values(by='Global_Sales', ascending=False)

    ct1=str(len(df_platform)) + " шт."
    ct2=str(df_platform['Global_Sales'].sum().round(2)) + " млн. $"
    ct3=str(popular_games['Name'].iloc[0])

    t = popular_games.iloc[0:8][['Name', 'Genre', 'Global_Sales']]
    t.rename(columns={'Name': 'Название', 'Genre': 'Жанр', 'Global_Sales': 'Продажи, млн. $'}, inplace=True)

    table1 = dbc.Table.from_dataframe(
        t, striped=True, bordered=True, hover=True, index=False)
    
    genre_counts = df_platform['Genre'].value_counts().reset_index()
    genre_counts.columns = ['Genre', 'Count']

    figure = px.pie(genre_counts, values='Count', names='Genre', height=500, width=650)
    figure.update_layout(margin=dict(t=15))

    return ct1, ct2, ct3, table1, figure