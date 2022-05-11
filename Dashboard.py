from  dash import Dash,html,dcc
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
pd.options.display.float_format = "{:,.2f}".format
from numpy import isin, outer
import figures as f

app = Dash(
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)

app.title='Esports Earnings'


games    = f.df_games.sort_values('TotalEarnings', ascending=False).head(1)

game     = games['Game']
game_val = "$" + str( "{:.2f}".format(float(games['TotalEarnings'] / 1000000)) ) + " M"

# Card 1 - for Main plot
card_content_total = [
    dbc.CardBody(
        [
            dbc.Row([
                dbc.Col([
                    html.Img(src="/assets/images/money.png", className="w-100")
                ], md=3),

                dbc.Col([
                    html.Div([
                        html.Div(game, className="text-dark", id='out'),
                        html.Div("Total Earnings", className="text-muted font_size"),
                        html.Div(game_val, className="big_decimal_total font_size_large", id='out2')
                    ], className="px-3 ", id='my-output'),
                ], className="", md=9)
            ])
        ]
    ),
]

card_content_games = [
    dbc.CardBody(
        [
            dbc.Row([
                dbc.Col([
                    html.Img(src="/assets/images/game_2.png", className="w-100")
                ], md=3),

                dbc.Col([
                    html.Div([
                        html.Div(game, className="text-dark", id='out3'),
                        html.Div("Most Popular Games", className="text-muted font_size"),
                        html.Div(game_val, className="big_decimal_games font_size_large", id='out4')
                    ], className="px-3 "),
                ], className="", md=9 ),
            ])
        ]
    ),
]


card_content_genres = [
    dbc.CardBody(
        [
            dbc.Row([
                dbc.Col([
                    html.Img(src="/assets/images/genre.png", className="w-100")
                ], md=3),

                dbc.Col([
                    html.Div([
                        html.Div("First-Person Shooter", className="text-dark"),
                        html.Div("Most Popular Genres - Among Players", className="text-muted font_size"),
                        html.Div("34.9 %", className="big_decimal_genres font_size_large")
                    ], className="px-3 "),
                ], className="", md=9 ),
            ])
        ]
    ),
]



app.layout = html.Div(
    [
        # First Row - Header and Filter and Switch
        dbc.Row([
            # Header
            dbc.Col(
                html.H3('Esports Earnings 1981 - 2021', className='text-dark'), md=9
            ),
            # Dropdown - Release date
            dbc.Col([
                html.Div([ 
                    html.Span('Release date: ', className='m-auto text-muted'),
                    dcc.Dropdown(['All Eras', '90s Era', '2000s Era', '2010s Era'], 'All Eras', id='years-dropdown', 
                        className='ml-5 w-100', clearable=False,
                    ),
                ])
            ], md=3)
        ],
            className='py-4'
        ),
        # End of Header Row
         
        # Second Row - Cards Row
        dbc.Row(
            [
                # Total Earning Card
                dbc.Col(
                    dbc.Card(
                        card_content_total,
                        className="total_card_color", 
                        inverse=True)
                ),
                dbc.Col(
                    dbc.Card(card_content_games, className="games_card_color", inverse=True)
                ),
                dbc.Col(dbc.Card(card_content_genres, className="genres_card_color", inverse=True)),
            ],
            className="mb-4",
        ),


        # Third Row - Plots
        dbc.Row(
            [
                dbc.Col([
                    dbc.Row([
                        dbc.Col([
                            html.H5("Total vs Online Earnings", 
                                className="my-4"),
                        ], md=7),
                        dbc.Col([
                            html.Span('Filter by: ', className='m-auto text-muted'),
                            dcc.Dropdown(['All','Multiplayer Online Battle Arena', 'First-Person Shooter',
                                'Battle Royale', 'Strategy', 'Collectible Card Game', 'Sports', 'Role-Playing Game',
                                'Fighting Game', 'Third-Person Shooter', 'Racing',
                                'Puzzle Game'],
                                'All',                         
                                clearable=False,
                                id='genres-dropdown', 
                                className='my-4'
                    ),
                        ], md=5),
                    ]),
                    
                    dbc.Row([
                        dcc.Graph(figure=f.fig, id="Graph1")
                    ]),
                ], md=8),
                
                
                dbc.Col([
                    dbc.Row([
                        dbc.Col([
                            html.H5("Most Popular:", 
                                className="my-4"),
                        ], md=6),
                        dbc.Col([
                            dcc.Dropdown([
                                'TotalPlayers',
                                'TotalTournaments',
                                'AvgPlayerTourment',
                                'AvgEarningsTourment',
                                'TotalEarnings',
                                'OnlineEarnings'],
                                'TotalPlayers', 
                                clearable=False,
                                id='games-dropdown', 
                                className='my-4'
                    ),
                        ], md=6),
                    ]),

                    dbc.Row([
                        html.Div(
                            dcc.Graph(figure=f.fig2, id="Graph2", className="mb-2")
                        )
                    ]),
                    dbc.Row([
                        dcc.Graph(figure=f.fig3, id="Graph3")
                    ]),
                ], md=4),
            ]
        ),
    ],
    className='container'
)

# Call back for interactivity
@app.callback(
    Output('Graph1', 'figure'),
    Output('Graph2', 'figure'),
    Output('out', 'children'),
    Output('out2', 'children'),
    Output('out3', 'children'),
    Output('out4', 'children'),
    Input('years-dropdown', 'value'),
    Input('genres-dropdown', 'value'),
    Input('games-dropdown', 'value'),
)
def update_output_div(value, value2, value3):
    if value == "All Eras":
        value = "1981-2021"
    elif value == "90s Era":
        value = "1981-2000"
    elif value == "2000s Era":
        value = "2001-2010"
    elif value == "2010s Era":
            value = "2011-2021"
    
    if value2 == "All":
        filtered = f.df_games[(f.df_games["ReleaseDate"] >= int(value[:4]) ) & (f.df_games["ReleaseDate"] <= int(value[5:]) )]
    else:
        filtered = f.df_games[(f.df_games["ReleaseDate"] >= int(value[:4]) ) & (f.df_games["ReleaseDate"] <= int(value[5:]) )]
        filtered = filtered[filtered["Genre"] == value2]
    
    games    = filtered.sort_values('TotalEarnings', ascending=False).head(1)
    game     = games['Game']
    game_val = "$" + str( "{:.2f}".format(float(games['TotalEarnings'] / 1000000)) ) + " M"

    top_10_games = filtered.sort_values('TotalEarnings', ascending=False).head(10)
    top_5_games = top_10_games.sort_values('TotalEarnings').tail(5)
    low_5_games = top_10_games.sort_values('TotalEarnings', ascending=False).tail(5)
    top_10_games = pd.concat([top_5_games, low_5_games], axis=0)
    fig = go.Figure()
    fig.add_trace(go.Bar(x=top_10_games['Game'],
                    y=top_10_games['TotalEarnings'],
                    name='TotalEarnings',
                    marker=dict(color = ['rgba(33, 81, 197, 0.8)',
                                        'rgba(33, 81, 197, 0.8)',
                                        'rgba(33, 81, 197, 0.8)',
                                        'rgba(33, 81, 197, 0.8)',
                                        'rgba(33, 81, 197, 1)',
                                        'rgba(33, 81, 197, 0.8)',
                                        'rgba(33, 81, 197, 0.8)',
                                        'rgba(33, 81, 197, 0.8)',
                                        'rgba(33, 81, 197, 0.8)',
                                        'rgba(33, 81, 197, 0.8)']),
                    ))

    fig.add_trace(go.Bar(x=top_10_games['Game'],
                    y=top_10_games['OnlineEarnings'],
                    name='OnlineEarnings',
                    marker=dict(color = ['rgba(227, 238, 253, 0.8)',
                                    'rgba(227, 238, 253, 0.8)',
                                    'rgba(227, 238, 253, 0.8)',
                                    'rgba(227, 238, 253, 0.8)',
                                    'rgba(227, 238, 253, 1)',
                                    'rgba(227, 238, 253, 0.8)',
                                    'rgba(227, 238, 253, 0.8)',
                                    'rgba(227, 238, 253, 0.8)',
                                    'rgba(227, 238, 253, 0.8)',
                                    'rgba(227, 238, 253, 0.8)']),
                    ))

    fig.update_layout(
        height=450,
        plot_bgcolor= '#fff',
        hovermode='closest',
        margin=dict(l=10,r=10,b=20,t=10),
        margin_pad=10,
        titlefont_size=14,
        xaxis_tickfont_size=8,
        yaxis=dict(
            title='USD (millions)',
            titlefont_size=10,
            tickfont_size=10,
        ),
        legend=dict(
            x=0,
            y=1.0,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)',
            
        ),
        barmode='group',
        bargap=0.25, # gap between bars of adjacent location coordinates.
        bargroupgap=0.15 # gap between bars of the same location coordinate.
    )
    
    filtered_2 = f.df_games[(f.df_games["ReleaseDate"] >= int(value[:4]) ) & (f.df_games["ReleaseDate"] <= int(value[5:]) )]

    games_2    = filtered_2.sort_values(value3, ascending=False).head(1)
    print(games_2)
    game_2     = games_2['Game']

    if value3 in ["TotalEarnings", "OnlineEarnings"]:
        game_val_2 = "$" + str( "{:.2f}".format(float(games_2[value3] / 1000000)) ) + " M"
    elif value3 in ["TotalPlayers", "TotalTournaments"]:
        game_val_2 = str( "{:.2f}".format(float(games_2[value3] / 1000)) ) + " K"
    elif value3 == "AvgPlayerTourment":
        game_val_2 = str( int(games_2[value3])) + " P/T"
    elif value3 == "AvgEarningsPlayer":
        game_val_2 = str( "{:.2f}".format(int(games_2[value3] / 1000)) ) + " K"
    elif value3 == "AvgEarningsTourment":
        game_val_2 = str( "{:.2f}".format(int(games_2[value3] / 1000)) ) + " K"

    popular_5_games = filtered_2.sort_values(value3, ascending=False).head()
    popular_3_games = popular_5_games.sort_values(value3).tail(3)
    popular_2_games = popular_5_games.sort_values(value3, ascending=False).tail(2)
    popular_5_games = pd.concat([popular_3_games, popular_2_games], axis=0)

    print(popular_5_games)

    fig2 = go.Figure(go.Bar(
                x=popular_5_games[value3],
                y=popular_5_games["Game"],
                marker=dict(color = ['rgba(95, 195, 144, 1)',
                                    'rgba(235, 254, 238, 1)',
                                    'rgba(95, 195, 144, 1)',
                                    'rgba(235, 254, 238, 1)',
                                    'rgba(95, 195, 144, 1)',]),
                orientation='h'))

    fig2.update_layout(
        title='Games',
        height=215,
        plot_bgcolor= '#fff',
        hovermode='closest',
        margin=dict(l=10,r=10,b=20,t=50),
        margin_pad=10,
        titlefont_size=14,
        xaxis_tickfont_size=8,
        yaxis=dict(
            titlefont_size=10,
            tickfont_size=10,
        ),
        legend=dict(
            x=0,
            y=1.0,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)',
            
        ),
        barmode='group',
        bargap=0.01, # gap between bars of adjacent location coordinates.
        bargroupgap=0.15 # gap between bars of the same location coordinate.
    )


    
    return (fig,fig2, game, game_val, game_2, game_val_2)
    

if __name__ == "__main__":
    app.run_server()