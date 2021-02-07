import dash
import dash_table
import dash_core_components as dcc 
import dash_html_components as html 
from dash.dependencies import Output, Input, State
import plotly.express as px
import dash_bootstrap_components as dbc 
import pandas as pd 
import pandas_datareader.data as web
import datetime

start_date = datetime.datetime.now() - datetime.timedelta(days=365) # datetime.datetime(2020, 1, 1)
end_date = datetime.datetime.now()  # datetime.date.today() # datetime.datetime(2020, 12, 3)
df = web.DataReader(['AMZN', 'GOOGL', 'FB', 'PFE', 'MRNA', 'BNTX'], 'stooq', \
    start=start_date, end=end_date)
df = df.stack().reset_index()
# df.to_csv('./data/stocks.csv', index=False)

#df = pd.read_csv('./data/stocks.csv')

# https://www.bootstrapcdn.com/bootswatch/
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
    meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1.0'}]
)

app.layout = dbc.Container([
    dbc.Row(
        dbc.Col(
            html.H1('Stock Market Dashboard', 
                className='text-center text-primary b-4'),
            width=12
            )
    ),

    # 2nd row
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(id='my-dpdn', multi=False, value='AMZN',\
                options = [{'label':x, 'value':x} for x in sorted(df['Symbols'].unique())]
            ),

            dcc.Graph(id='line-fig', figure={})
        ], xs=12, sm=12, md=12, lg=5, xl=5),  #width={'size':5, 'order':1, 'offset':0}

        dbc.Col([
            dcc.Dropdown(
                id='my-dpdn2', multi=True, value=['PFE','BNTX'],
                options = [{'label':x, 'value':x} for x in sorted(df['Symbols'].unique())]
            ), 

            dcc.Graph(id='line-fig2', figure={})             

        ], xs=12, sm=12, md=12, lg=5, xl=5),

    ], no_gutters=True, justify='start'),

    # 3rd row
    dbc.Row([
        dbc.Col([
            html.P("Select Company Stock: ", style={'textDecoration':'underline'}),
            dcc.Checklist(
                id='my-checklist', value=['FB','GOOGL','AMZN'],
                options = [{'label':x, 'value':x} for x in sorted(df['Symbols'].unique())]),
            dcc.Graph(id='my-hist', figure={})
        ], xs=12, sm=12, md=12, lg=5, xl=5),

        dbc.Col([
            dbc.Card(
                [
                    dbc.CardHeader(
                        dbc.Button("Show the Org-Chart", color="link", id='btn-org-chart')
                    ),
                    dbc.Collapse([
                        dbc.CardBody(
                        html.P("Fujitsu Org-Chart", className='card-text'),
                        ),

                        dbc.CardImg(
                            src="./assets/org.gif", bottom=True
                        )], id="coll-btn", is_open=False
                    ),
                ], style={'width': "24rem"}
            )
        ], xs=12, sm=12, md=12, lg=5, xl=5)
    ], align='center'), #Vertical: start, center, end

    # 4th row for data table
    dbc.Row(
        dbc.Col(
            dash_table.DataTable(
                id='datatable_id',
                data=df.to_dict('records'),
                columns=[
                    {"name": i, "id": i, "deletable": False, "selectable": False} for i in df.columns
                ],
                editable=False,
                filter_action="native",
                page_size=15,
                page_current=0,
                page_action="native",
                selected_rows=[],
                row_deletable=False,
                row_selectable=None,
                sort_action="native"
            )
        )
    )
], fluid=True)

##################### callback ######################
# line chart
@app.callback(
    Output('line-fig', 'figure'),
    Input('my-dpdn', 'value')
)
def update_graph(stock_slctd):
    df_filter = df[df['Symbols']==stock_slctd]
    return px.line(df_filter, x='Date', y='High')

# line chart 2
@app.callback(
    Output('line-fig2', 'figure'),
    Input('my-dpdn2', 'value')
)
def update_graph(stock_slctd):
    df_filter = df[df['Symbols'].isin(stock_slctd)]
    return px.line(df_filter, x='Date', y='Open', color='Symbols')

# histogram chart
@app.callback(
    Output('my-hist', 'figure'),
    Input('my-checklist', 'value')
)
def update_graph(stock_slctd):
    df_filter = df[df['Symbols'].isin(stock_slctd)]
    df_filter = df_filter[df_filter['Date']=='2020-12-03']
    return px.histogram(df_filter, x='Symbols', y='Close')

@app.callback(
    Output("coll-btn", "is_open"),
    [Input("btn-org-chart","n_clicks")],
    [State("coll-btn", "is_open")]
)
def update_state(n, is_open):
    if n:
        return not is_open
    return is_open



if __name__ == '__main__':
    app.run_server(port=3000, debug=False)

