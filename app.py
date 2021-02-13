# Imports
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt
from dash.dependencies import Input, Output
from app_utils import *

# Define some global variables
list_equipment = ['Raw', 'Wraps', 'Single-ply', 'Multi-ply']
list_classes = ['IPF', 'WRPF']
list_columns = ['Date', 'Meet', 'Federation', 'ParentFederation', 'WeightClass',
                'Squat1', 'Squat2', 'Squat3', 'Squat',
                'Bench1', 'Bench2', 'Bench3', 'Bench',
                'Deadlift1', 'Deadlift2', 'Deadlift3', 'Deadlift',
                'Total', 'Wilks'
                ]

# Load data
data = load_data()

# Initialize the app
app = dash.Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])

# Define the layout
app.layout = html.Div(children=[
    dcc.Tabs([

        # Tab for global stats:
        # * Menus to select options
        # * Plot with top squats per sex and weight class
        # * Plot with top benches per sex and weight class
        # * Plot with top deadlifts per sex and weight class
        # * Plot with top totals per sex and weight class
        # * Plot with top wilks per sex and weight class
        dcc.Tab(
            id='tab-global',
            label='Global stats',
            children=[
                # Dropdown menus to select options
                html.Div(children=[

                    # Menu for equipment
                    html.Div(children=[
                        html.H3(children="Equipment:"),
                        dcc.Dropdown(id='globalstats-dropdown-equipment',
                                     options=[{'label': i, 'value': i} for i in list_equipment],
                                     value=['Raw'],
                                     multi=True
                                     )
                    ], className='four columns'),

                    # Menu for weight classes
                    html.Div(children=[
                        html.H3(children="Weight classes"),
                        dcc.Dropdown(id='globalstats-dropdown-weight_classes',
                                     options=[{'label': i, 'value': i} for i in list_classes],
                                     value='IPF'
                                     )
                    ], className='four columns'),

                    # Menu for number of lifters
                    html.Div(children=[
                        html.H3(children="Lifters per class:"),
                        dcc.Slider(id='globalstats-slider-top',
                                   min=1,
                                   max=100,
                                   marks={10 * i: str(10 * i) for i in range(1, 10)},
                                   value=10
                                   )
                    ], className='four columns')
                ], className='row'),

                # Plots
                html.Div(children=dcc.Graph(id='globalstats-graph-men')),
                html.Div(children=dcc.Graph(id='globalstats-graph-women'))

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

                # Plots
                html.Div(children=dcc.Graph(id='lifterstats-graph-evolution')),

                # Table with the data of the meets
                dt.DataTable(
                    id='lifterstats-datatable-meets',
                    columns=[{'id': col, 'name': col} for col in list_columns],
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
    Output('globalstats-graph-men', 'figure'),
    [Input('globalstats-dropdown-weight_classes', 'value'),
     Input('globalstats-dropdown-equipment', 'value'),
     Input('globalstats-slider-top', 'value')]
    )
def display_globalstats_graph_men(classes, equipment, n):
    """
    Plot best lifts for men lifters.

    :param str classes: federation to take weight classes from. 'IPF' or 'WRPF'.
    :param list equipment: allowed equipment for the meets. 'Raw', 'Wraps', 'Single-ply' or 'Multi-ply'.
    :param int n: number of lifters to keep of each weight class.
    :return fig: Figure, figure with the plot.
    """
    # Load and clean data
    df = clean_data(data, classes, equipment)

    # Make the figure
    fig = plot_best_lifts_per_weightclass(df, 'M', classes, n)

    return fig


@app.callback(
    Output('globalstats-graph-women', 'figure'),
    [Input('globalstats-dropdown-weight_classes', 'value'),
     Input('globalstats-dropdown-equipment', 'value'),
     Input('globalstats-slider-top', 'value')])
def display_globalstats_graph_women(classes, equipment, n):
    """
    Plot best lifts for women lifters.

    :param str classes: federation to take weight classes from. 'IPF' or 'WRPF'.
    :param list equipment: allowed equipment for the meets. 'Raw', 'Wraps', 'Single-ply' or 'Multi-ply'.
    :param int n: number of lifters to keep of each weight class.
    :return fig: Figure, figure with the plot.
    """
    # Load and clean data
    df = clean_data(data, classes, equipment)

    # Make the figure
    fig = plot_best_lifts_per_weightclass(df, 'F', classes, n)

    return fig


@app.callback(
    Output('lifterstats-graph-evolution', 'figure'),
    [Input('lifterstats-dropdown-name', 'value')])
def display_lifterstats_graph_evolution(name):
    """
    Filter meet data for a lifter and plot evolution for the squat.

    :param str name: name of the lifter.
    :return fig: Figure, figure with the plot.
    """
    # Make the figure
    fig = plot_lift_evolution_per_lifter(data, name)

    return fig


@app.callback(
    Output('lifterstats-datatable-meets', 'data'),
    [Input('lifterstats-dropdown-name', 'value')])
def display_lifterstats_table_meets(name):
    """
    Filter meet data for a lifter and sort it by date.

    :param str name: name of the lifter.
    :return: dict, meet data in record format.
    """
    # Make the table
    table = table_meets_per_lifter(data, name)

    return table


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
