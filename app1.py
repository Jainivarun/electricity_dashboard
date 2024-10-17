import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output
import plotly.graph_objects as go

#reading and processing data using pandas
weather=pd.read_csv("C:\\Users\\Dell\\Music\\Downloads\\weather_data.csv")  
demand=pd.read_csv("C:\\Users\\Dell\\Music\\Downloads\\electricity_demand.csv")

#initilaizing dashboard
app = dash.Dash()

#dashboard layout
app.layout = html.Div(children=[
    html.H1("Electricity Demand at Chennai city(TNEB)",style={'color':'blue','text-align':'center','background-color':'yellow','text-decoration':'underline'}),
    dcc.Graph(id='demand-graph',
              animate=True
              ),
    html.H2("Impact of weather on demand",style={'color':'blue','text-align':'center','background-color':'yellow','text-decoration':'underline'}),
    html.Div("Select the weather element except date string:",style={'font-family':'bold','font-size':'20px'}),
    dcc.Dropdown(
        id='weather-select',
        options=[{'label': col, 'value': col} for col in weather.columns if col != 'datestamp'],
        value='temp',
        
    ),
    dcc.Graph(id='graph'),
 html.H3("Weather Data Table",style={'color':'blue','text-align':'center','background-color':'yellow','text-decoration':'underline'}),
    html.Table([
        html.Tr([html.Th(col) for col in weather.columns],style={'border':'4px solid black','text-align':'center'}),
        html.Tbody(id='weather-table')
    ],style={'border':'4px solid black','border-radius':'10px'})
],style={'background-color':'yellow','text-align':'center','font-size':'20','width':'100%','border-collapse':'collapse'})

#callback for electricity demand graph
@app.callback(
    Output('demand-graph', 'figure'),
    Input('weather-select', 'value')
)
def update_demand_graph(selected_weather):
    fig = px.line(demand, x='datetime', y=['current_demand', 'predicted_demand','previously_predicted_demand'],
                  title='current vs future predicted vs previously predicted electricity demand')
    return fig

#callback for weather graph
@app.callback(
    Output('graph', 'figure'),
    [Input('weather-select', 'value')]
)
def update_weather_graph(selected_weather):
    fig = px.bar(weather, x='datestamp', y=selected_weather ,title=f'datestamp vs {selected_weather} Graph')
    return fig

#callback for weather table
@app.callback(
    Output('weather-table', 'children'),
    [Input('weather-select', 'value')]
)
def update_weather_table(selected_weather):
    temp1= [html.Tr([html.Td(weather.iloc[i][col]) for col in weather.columns],style={'padding':'15px'}) for i in range(len(weather))]
    return temp1
if __name__ == '__main__':
    app.run_server()

