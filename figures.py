from  dash import Dash,html,dcc
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
pd.options.display.float_format = "{:,.2f}".format
from numpy import outer


########################## Main Plot - Bar Plot ###########################
# Load Datasets
df_games = pd.read_csv('Data/Games.csv', encoding='cp1252')
df_genres = pd.read_csv('Data/Genres.csv', encoding='cp1252')

top_10_games = df_games.sort_values('TotalEarnings', ascending=False).head(10)
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
    margin=dict(l=10,r=10,b=20,t=50),
    margin_pad=10,
    title='Total earnings vs Online earnings Top 10 Games',
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









########################## Horizontal Bar Plot - Second Fig ################ 
popular_5_games = df_games.head()
popular_3_games = popular_5_games.sort_values('TotalEarnings').tail(3)
popular_2_games = popular_5_games.sort_values('TotalEarnings', ascending=False).tail(2)
popular_5_games = pd.concat([popular_3_games, popular_2_games], axis=0)

popular_5_games

fig2 = go.Figure(go.Bar(
            x=popular_5_games["TotalEarnings"],
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



##################### Pie Chart - Fig 3 #####################
df_genres = df_genres.sort_values("TotalPlayers", ascending=False)
labels = df_genres["Genre"].head(6).to_list()
values = df_genres["TotalTournaments"].head(6).to_list()
colors = ['#A63A50','#F0E7D8','#AB9B96','#A1674A', '#BA6E6E', '#F8EAE3']

# pull is given as a fraction of the pie radius
fig3 = go.Figure(data=
                [go.Pie(labels=labels,
                             values=values,
                             pull=[0.05, 0.05, 0.05, 0.05, 0.05, 0.05],
                             marker_colors = colors,
                            )])

fig3.update_traces(textposition='inside')

fig3.update_layout(
    title='Genres',
    height=225,
    plot_bgcolor= '#fff',
    hovermode='closest',
    margin=dict(l=10,r=10,b=20,t=50),
    margin_pad=10,
    titlefont_size=14,
),