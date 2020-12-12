# Imports
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt
from dash.dependencies import Input, Output
from app_utils import *
import pandas as pd


# Load data
data = load_data('data/openpowerlifting-2020-10-16/openpowerlifting-2020-10-16.csv')

# Initialize the app
app = dash.Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])

# Define the layout
app.layout = html.Div(children=[
    dcc.Tabs([

        # Tab for global stats:
        # * Menus to select options
        # * Plot with best men squat per weight class
        # * Plot with best men bench per weight class
        # * Plot with best men deadlift per weight class
        # * Plot with best women squat per weight class
        # * Plot with best women bench per weight class
        # * Plot with best women deadlift per weight class
        dcc.Tab(
            id='tab-global',
            label='Global stats',
            children=[
                # Dropdown menus to select options
                html.Div(children=[
                    html.Div(children=[
                        html.H3(children="Weight classes to use:"),
                        dcc.Dropdown(id='globalstats-dropdown-weight_classes',
                                     options=[{'label': i, 'value': i} for i in ['IPF', 'WRPF']],
                                     value='IPF'
                                     )
                    ], className='four columns'),

                    html.Div(children=[
                        html.H3(children="Equipment:"),
                        dcc.Dropdown(id='globalstats-dropdown-equipment',
                                     options=[{'label': i, 'value': i} for i in ['Raw', 'Raw+Wraps']],
                                     value='Raw'
                                     )
                    ], className='four columns'),

                    html.Div(children=[
                        html.H3(children="Lifters per class to show:"),
                        dcc.Slider(id='globalstats-slider-top',
                                   min=1,
                                   max=100,
                                   marks={10 * i: str(10 * i) for i in range(1, 10)},
                                   value=10
                                   )
                    ], className='four columns')
                ], className='row'),

                # Plots with best squat, bench and deadlift per weight class
                html.Div(children=[
                    html.Div(children=dcc.Graph(id='globalstats-graph-men-squat'), className='three columns'),
                    html.Div(children=dcc.Graph(id='globalstats-graph-men-bench'), className='three columns'),
                    html.Div(children=dcc.Graph(id='globalstats-graph-men-deadlift'), className='three columns'),
                    html.Div(children=dcc.Graph(id='globalstats-graph-men-total'), className='three columns')
                ], className='row'),

                html.Div(children=[
                    html.Div(children=dcc.Graph(id='globalstats-graph-women-squat'), className='three columns'),
                    html.Div(children=dcc.Graph(id='globalstats-graph-women-bench'), className='three columns'),
                    html.Div(children=dcc.Graph(id='globalstats-graph-women-deadlift'), className='three columns'),
                    html.Div(children=dcc.Graph(id='globalstats-graph-women-total'), className='three columns')
                ], className='row')

            ]
        ),

        # Tab for lifter stats:
        # * Dropdown menu to select the lifter
        # * Plot with squat evolution
        # * Plot with bench evolution
        # * Plot with deadlift evolution
        # * Table with meet data
        dcc.Tab(
            id='tab-lifterstats',
            label='Lifter stats',
            children=[
                # Dropdown menu to select the lifter
                dcc.Dropdown(
                    id='lifterstats-dropdown-name',
                    options=[{'label': name, 'value': name} for name in data['Name'].unique().tolist()],
                    value='Taylor Atwood'
                ),

                # Plots with the evolutions of squat, bench and deadlift
                html.Div(children=[
                    html.Div(children=dcc.Graph(id='lifterstats-graph-squat'), className='four columns'),
                    html.Div(children=dcc.Graph(id='lifterstats-graph-bench'), className='four columns'),
                    html.Div(children=dcc.Graph(id='lifterstats-graph-deadlift'), className='four columns')
                ], className='row'),

                # Table with the data of the meets
                dt.DataTable(
                    id='lifterstats-datatable-meets',
                    columns=[{'id': col, 'name': col} for col in data.columns.values],
                    style_table={'overflowX': 'auto'},
                    page_size=10,
                    style_data_conditional=[
                        {
                            'if': {'row_index': 'odd'},
                            'backgroundColor': 'rgb(248, 248, 248)'
                        }
                    ],
                    style_header={
                        'backgroundColor': 'rgb(230, 230, 230)',
                        'fontWeight': 'bold'
                    }
                )
            ]
        )
    ])
])


# Define the callbacks
@app.callback(
    Output('globalstats-graph-men-squat', 'figure'),
    [Input('globalstats-dropdown-weight_classes', 'value'),
     Input('globalstats-dropdown-equipment', 'value'),
     Input('globalstats-slider-top', 'value')])
def display_globalstats_graph_men_squat(federation, equipment, n):
    """
    Plot best squat for each men lifter.

    :return fig: (dict) figure with the plot.
    """
    # Load and clean data
    df = clean_data(data, federation, equipment)

    # Obtain best squat per men lifter and group by weight class
    df_squat = get_best_lifts_per_weightclass(df,
                                              lift='SquatBest',
                                              sex='M',
                                              n=n
                                              )

    # Make the figure
    fig = plot_best_lifts_per_weightclass(data=df_squat,
                                          lift='SquatBest',
                                          sex='M',
                                          federation=federation,
                                          title='<b>Squat</b>'
                                          )

    return fig


@app.callback(
    Output('globalstats-graph-men-bench', 'figure'),
    [Input('globalstats-dropdown-weight_classes', 'value'),
     Input('globalstats-dropdown-equipment', 'value'),
     Input('globalstats-slider-top', 'value')])
def display_globalstats_graph_men_bench(federation, equipment, n):
    """
    Plot best bench for each men lifter.

    :return fig: (dict) figure with the plot.
    """
    # Load and clean data
    df = clean_data(data, federation, equipment)

    # Obtain best bench per men lifter and group by weight class
    df_bench = get_best_lifts_per_weightclass(df,
                                              lift='BenchBest',
                                              sex='M',
                                              n=n
                                              )

    # Make the figure
    fig = plot_best_lifts_per_weightclass(data=df_bench,
                                          lift='BenchBest',
                                          sex='M',
                                          federation=federation,
                                          title='<b>Bench</b>',
                                          )

    return fig


@app.callback(
    Output('globalstats-graph-men-deadlift', 'figure'),
    [Input('globalstats-dropdown-weight_classes', 'value'),
     Input('globalstats-dropdown-equipment', 'value'),
     Input('globalstats-slider-top', 'value')])
def display_globalstats_graph_men_deadlift(federation, equipment, n):
    """
    Plot best deadlift for each men lifter.

    :return fig: (dict) figure with the plot.
    """
    # Load and clean data
    df = clean_data(data, federation, equipment)

    # Obtain best deadlift per men lifter and group by weight class
    df_deadlift = get_best_lifts_per_weightclass(df,
                                                 lift='DeadliftBest',
                                                 sex='M',
                                                 n=n
                                                 )

    # Make the figure
    fig = plot_best_lifts_per_weightclass(data=df_deadlift,
                                          lift='DeadliftBest',
                                          sex='M',
                                          federation=federation,
                                          title='<b>Deadlift</b>'
                                          )

    return fig


@app.callback(
    Output('globalstats-graph-men-total', 'figure'),
    [Input('globalstats-dropdown-weight_classes', 'value'),
     Input('globalstats-dropdown-equipment', 'value'),
     Input('globalstats-slider-top', 'value')])
def display_globalstats_graph_men_total(federation, equipment, n):
    """
    Plot best deadlift for each men lifter.

    :return fig: (dict) figure with the plot.
    """
    # Load and clean data
    df = clean_data(data, federation, equipment)

    # Obtain best deadlift per men lifter and group by weight class
    df_total = get_best_lifts_per_weightclass(df,
                                              lift='Total',
                                              sex='M',
                                              n=n
                                              )

    # Make the figure
    fig = plot_best_lifts_per_weightclass(data=df_total,
                                          lift='Total',
                                          sex='M',
                                          federation=federation,
                                          title='<b>Total</b>'
                                          )

    return fig


@app.callback(
    Output('globalstats-graph-women-squat', 'figure'),
    [Input('globalstats-dropdown-weight_classes', 'value'),
     Input('globalstats-dropdown-equipment', 'value'),
     Input('globalstats-slider-top', 'value')])
def display_globalstats_graph_women_squat(federation, equipment, n):
    """
    Plot best squat for each women lifter.

    :return fig: (dict) figure with the plot.
    """
    # Load and clean data
    df = clean_data(data, federation, equipment)

    # Obtain best squat per women lifter and group by weight class
    df_squat = get_best_lifts_per_weightclass(df,
                                              lift='SquatBest',
                                              sex='F',
                                              n=n
                                              )

    # Make the figure
    fig = plot_best_lifts_per_weightclass(data=df_squat,
                                          lift='SquatBest',
                                          sex='F',
                                          federation=federation,
                                          title='<b>Squat</b>'
                                          )

    return fig


@app.callback(
    Output('globalstats-graph-women-bench', 'figure'),
    [Input('globalstats-dropdown-weight_classes', 'value'),
     Input('globalstats-dropdown-equipment', 'value'),
     Input('globalstats-slider-top', 'value')])
def display_globalstats_graph_women_bench(federation, equipment, n):
    """
    Plot best bench for each women lifter.

    :return fig: (dict) figure with the plot.
    """
    # Load and clean data
    df = clean_data(data, federation, equipment)

    # Obtain best bench per women lifter and group by weight class
    df_bench = get_best_lifts_per_weightclass(df,
                                              lift='BenchBest',
                                              sex='F',
                                              n=n
                                              )

    # Make the figure
    fig = plot_best_lifts_per_weightclass(data=df_bench,
                                          lift='BenchBest',
                                          sex='F',
                                          federation=federation,
                                          title='<b>Bench</b>',
                                          )

    return fig


@app.callback(
    Output('globalstats-graph-women-deadlift', 'figure'),
    [Input('globalstats-dropdown-weight_classes', 'value'),
     Input('globalstats-dropdown-equipment', 'value'),
     Input('globalstats-slider-top', 'value')])
def display_globalstats_graph_women_deadlift(federation, equipment, n):
    """
    Plot best deadlift for each women lifter.

    :return fig: (dict) figure with the plot.
    """
    # Load and clean data
    df = clean_data(data, federation, equipment)

    # Obtain best deadlift per women lifter and group by weight class
    df_deadlift = get_best_lifts_per_weightclass(df,
                                                 lift='DeadliftBest',
                                                 sex='F',
                                                 n=n
                                                 )

    # Make the figure
    fig = plot_best_lifts_per_weightclass(data=df_deadlift,
                                          lift='DeadliftBest',
                                          sex='F',
                                          federation=federation,
                                          title='<b>Deadlift</b>'
                                          )

    return fig


@app.callback(
    Output('globalstats-graph-women-total', 'figure'),
    [Input('globalstats-dropdown-weight_classes', 'value'),
     Input('globalstats-dropdown-equipment', 'value'),
     Input('globalstats-slider-top', 'value')])
def display_globalstats_graph_women_total(federation, equipment, n):
    """
    Plot best deadlift for each men lifter.

    :return fig: (dict) figure with the plot.
    """
    # Load and clean data
    df = clean_data(data, federation, equipment)

    # Obtain best deadlift per men lifter and group by weight class
    df_total = get_best_lifts_per_weightclass(df,
                                              lift='Total',
                                              sex='F',
                                              n=n
                                              )

    # Make the figure
    fig = plot_best_lifts_per_weightclass(data=df_total,
                                          lift='Total',
                                          sex='F',
                                          federation=federation,
                                          title='<b>Total</b>'
                                          )

    return fig


@app.callback(
    Output('lifterstats-datatable-meets', 'data'),
    [Input('lifterstats-dropdown-name', 'value')])
def display_lifterstats_table_meets(name: str):
    """
    Filter meet data for a lifter and sort it by date.

    :param name: (str) name of the lifter.
    :return df_records: (dict) meet data in record format.
    """
    # Filter data
    df = data[data['Name'] == name]

    # Sort by date
    df = df.sort_values(by='Date', ascending=False)

    # Obtain the records
    df_records = df.to_dict('records')

    return df_records


@app.callback(
    Output('lifterstats-graph-squat', 'figure'),
    [Input('lifterstats-dropdown-name', 'value')])
def display_lifterstats_graph_squat(name: str):
    """
    Filter meet data for a lifter and plot evolution for the squat.

    :param name: (str) name of the lifter.
    :return fig: (dict) figure with the plot.
    """
    # Filter data
    df = data[data['Name'] == name]

    # Sort by date
    df = df.sort_values(by='Date', ascending=False)

    # Make the figure
    fig = px.scatter(df,
                     x='Date',
                     y='SquatBest',
                     title='<b>Squat</b>',
                     hover_name='Meet',
                     hover_data=['Squat1', 'Squat2', 'Squat3']
                     )

    return fig.update_traces(mode='lines+markers')


@app.callback(
    Output('lifterstats-graph-bench', 'figure'),
    [Input('lifterstats-dropdown-name', 'value')])
def display_lifterstats_graph_bench(name: str):
    """
    Filter meet data for a lifter and plot evolution for the bench.

    :param name: (str) name of the lifter.
    :return fig: (dict) figure with the plot.
    """
    # Filter data
    df = data[data['Name'] == name]

    # Sort by date
    df = df.sort_values(by='Date', ascending=False)

    # Make the figure
    fig = px.scatter(df,
                     x='Date',
                     y='BenchBest',
                     title='<b>Bench</b>',
                     hover_name='Meet',
                     hover_data=['Bench1', 'Bench2', 'Bench3']
                     )

    return fig.update_traces(mode='lines+markers')


@app.callback(
    Output('lifterstats-graph-deadlift', 'figure'),
    [Input('lifterstats-dropdown-name', 'value')])
def display_lifterstats_graph_deadlift(name: str):
    """
    Filter meet data for a lifter and plot evolution for the deadlift.

    :param name: (str) name of the lifter.
    :return fig: (dict) figure with the plot.
    """
    # Filter data
    df = data[data['Name'] == name]

    # Sort by date
    df = df.sort_values(by='Date', ascending=False)

    # Make the figure
    fig = px.scatter(df,
                     x='Date',
                     y='DeadliftBest',
                     title='<b>Deadlift</b>',
                     hover_name='Meet',
                     hover_data=['Deadlift1', 'Deadlift2', 'Deadlift3']
                     )

    return fig.update_traces(mode='lines+markers')

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
