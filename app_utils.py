# Imports
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# Functions
def get_weight_classes(federation, sex):
    """
    Get weight classes for a given sex and federation.

    :param str federation: federation to take weight classes from. 'IPF' or 'WRPF'.
    :param str sex: sex to take weight classes from. 'M' or 'F'.
    :return list bins:
    :return list labels:
    """
    # Initialize values
    bins = []
    labels = []

    # Update values
    if federation == 'IPF':
        if sex == 'M':
            bins = [0.0, 59.0, 66.0, 74.0, 83.0, 93.0, 105.0, 120.0, 1000.0]
            labels = ['59', '66', '74', '83', '93', '105', '120', '120+']
        elif sex == 'F':
            bins = [0.0, 47.0, 52.0, 57.0, 63.0, 72.0, 84.0, 1000.0]
            labels = ['47', '52', '57', '63', '72', '84', '84+']

    elif federation == 'WRPF':
        if sex == 'M':
            bins = [0.0, 56.0, 60.0, 67.5, 75.0, 82.5, 90.0, 100.0, 110.0, 125.0, 140.0, 1000.0]
            labels = ['56', '60', '67.5', '75', '82.5', '90', '100', '110', '125', '140', '140+']
        elif sex == 'F':
            bins = [0.0, 44.0, 48.0, 52.0, 56.0, 60.0, 67.5, 75.0, 82.5, 90.0, 1000.0]
            labels = ['44', '48', '52', '56', '60', '67.5 ', '75', '82.5', '90', '90+']

    return bins, labels


def download_data():
    a = 1
    return a


def load_data(path):
    # Load data
    data = pd.read_csv(path,
                       header=0,
                       names=['Name',
                              'Sex',
                              'Event',
                              'Equipment',
                              'Age',
                              'AgeClass',
                              'BirthYearClass',  #
                              'Division',
                              'Bodyweight',  # 'Bodyweight'
                              'WeightClass',  # 'WeightClassKg'
                              'Squat1',  # 'Squat1Kg'
                              'Squat2',  # 'Squat2Kg'
                              'Squat3',  # 'Squat3Kg'
                              'Squat4',  # 'Squat4Kg'
                              'Squat',  # 'Best3SquatKg'
                              'Bench1',  # 'Bench1Kg'
                              'Bench2',  # 'Bench2Kg'
                              'Bench3',  # 'Bench3Kg'
                              'Bench4',  # 'Bench4Kg'
                              'Bench',  # 'Best3BenchKg'
                              'Deadlift1',  # 'Deadlift1Kg'
                              'Deadlift2',  # 'Deadlift2Kg'
                              'Deadlift3',  # 'Deadlift3Kg'
                              'Deadlift4',  # 'Deadlift4Kg'
                              'Deadlift',  # 'Best3DeadliftKg'
                              'Total',  # 'TotalKg'
                              'Place',
                              'Dots',
                              'Wilks',
                              'Glossbrenner',
                              'Goodlift',
                              'Tested',
                              'Country',
                              'Federation',
                              'ParentFederation',
                              'Date',
                              'MeetCountry',
                              'MeetState',
                              'MeetTown',
                              'Meet'  # 'MeetName'
                              ],
                       usecols=['Name',
                                'Country',
                                'Sex',
                                'Age',
                                'Bodyweight',
                                'WeightClass',
                                'Date',
                                'Federation',
                                'ParentFederation',
                                'Meet',
                                'Event',
                                'Equipment',
                                'Squat1',
                                'Squat2',
                                'Squat3',
                                'Squat',
                                'Bench1',
                                'Bench2',
                                'Bench3',
                                'Bench',
                                'Deadlift1',
                                'Deadlift2',
                                'Deadlift3',
                                'Deadlift',
                                'Total',
                                'Wilks'
                                ],
                       dtype={'Name': 'str',
                              'Country': 'str',
                              'Sex': 'str',
                              'Age': 'float',
                              'Bodyweight': 'float',
                              'WeightClass': 'str',
                              'Federation': 'str',
                              'ParentFederation': 'str',
                              'Meet': 'str',
                              'Event': 'str',
                              'Equipment': 'str',
                              'Squat1': 'float',
                              'Squat2': 'float',
                              'Squat3': 'float',
                              'Squat': 'float',
                              'Bench1': 'float',
                              'Bench2': 'float',
                              'Bench3': 'float',
                              'Bench': 'float',
                              'Deadlift1': 'float',
                              'Deadlift2': 'float',
                              'Deadlift3': 'float',
                              'Deadlift': 'float',
                              'Total': 'float',
                              'Wilks': 'float'
                              },
                       parse_dates=['Date']
                       )

    # Perform some universal cleaning
    data = data.loc[data['Event'] == 'SBD']
    data = data.loc[data['Sex'] != 'Mx']
    #data = data.loc[data['Equipment'].isin(['Raw', 'Wraps'])]

    # Drop null values
    data = data.dropna(subset=['Squat', 'Bench', 'Deadlift', 'Total'])

    return data


def clean_data(data, federation, equipment):
    """
    Clean data using the filters selected by the user.

    :param pandas.DataFrame data: raw data from all the meets.
    :param federation:
    :param equipment:
    :return:
    """
    # Copy data
    df = data.copy()

    # Obtain weight classes
    men_bins, men_labels = get_weight_classes(federation=federation, sex='M')
    women_bins, women_labels = get_weight_classes(federation=federation, sex='F')

    # Clean weight classes
    df.loc[df['Sex'] == 'M', 'WeightClass'] = pd.cut(df.loc[df['Sex'] == 'M', 'Bodyweight'],
                                                     bins=men_bins,
                                                     labels=men_labels
                                                     )
    df.loc[df['Sex'] == 'F', 'WeightClass'] = pd.cut(df.loc[df['Sex'] == 'F', 'Bodyweight'],
                                                     bins=women_bins,
                                                     labels=women_labels
                                                     )

    # Filter by equipment
    df = df.loc[df['Equipment'].isin([x for x in equipment])]

    # Sort data
    df = df.sort_values(by='Wilks', ascending=False)

    return df


def get_best_lifts_per_weightclass(data, lift, sex, n=10):
    """
    Get n best lifts for weight class and sex.

    :param pandas.DataFrame data: raw data from all the meets.
    :param str sex: sex to filter. 'M' or 'F'.
    :param str lift: lift to track.
    :param int n: number of lifters to keep of each weight class.
    :return pandas.DataFrame df: data from n best lifts for weight class and sex.
    """
    # Perform the filter and the groupings
    df = data[data['Sex'] == sex] \
        .sort_values(by=['WeightClass', 'Name', lift], ascending=False) \
        .groupby(['WeightClass', 'Name'], as_index=False).first() \
        .sort_values(by=['WeightClass', lift], ascending=False) \
        .groupby('WeightClass', as_index=False).head(n)

    return df


def get_lift_plot_per_weightclass(fig, data, lift, weight_classes, colors, row, col, showlegend=False):
    """

    :param fig:
    :param data:
    :param lift:
    :param weight_classes:
    :param colors:
    :param row:
    :param col:
    :param showlegend:
    :return:
    """
    for i, wc in enumerate(weight_classes):
        df = data[data['WeightClass'] == wc]
        fig.add_trace(
            go.Scatter(x=df['Bodyweight'],
                       y=df[lift],
                       customdata=df['Date'],
                       mode='markers',
                       name=wc,
                       marker=dict(color=colors[i]),
                       hovertext=df['Name'],
                       hovertemplate='<b>%{hovertext}</b><br>Bodyweight: %{x} <br>' + lift + ': %{y}<br>Date: %{customdata|%Y-%m-%d}<extra></extra>',
                       legendgroup='WeightClass',
                       showlegend=showlegend
                       ),
            row=row,
            col=col
        )
    return fig


def plot_best_lifts_per_weightclass(data, sex, federation, n):
    """
    Plot n best lifts for weight class and sex.

    :param pandas.DataFrame data: data with n best lifts for weight class and sex.
    :param str sex: sex to filter. 'M' or 'F'.
    :param str federation: federation to take weight classes from. 'IPF' or 'WRPF'.
    :param int n: number of lifters to keep of each weight class.
    :return:
    """
    # Get weight classes
    _, weight_classes = get_weight_classes(federation=federation, sex=sex)

    # Get colors
    colors = px.colors.qualitative.Dark24

    # Get best lifts
    df_s = get_best_lifts_per_weightclass(data, lift='Squat', sex=sex, n=n)
    df_b = get_best_lifts_per_weightclass(data, lift='Bench', sex=sex, n=n)
    df_d = get_best_lifts_per_weightclass(data, lift='Deadlift', sex=sex, n=n)
    df_t = get_best_lifts_per_weightclass(data, lift='Total', sex=sex, n=n)
    df_w = get_best_lifts_per_weightclass(data, lift='Wilks', sex=sex, n=n)

    # Make figure
    fig = make_subplots(rows=1,
                        cols=5,
                        subplot_titles=['<b>Squat</b>', '<b>Bench</b>', '<b>Deadlift</b>', '<b>Total</b>', '<b>Wilks</b>']
                        )

    # Add plots of lifts
    fig = get_lift_plot_per_weightclass(fig,
                                        data=df_s,
                                        lift='Squat',
                                        weight_classes=weight_classes,
                                        colors=colors,
                                        row=1,
                                        col=1,
                                        showlegend=True
                                        )
    fig = get_lift_plot_per_weightclass(fig,
                                        data=df_b,
                                        lift='Bench',
                                        weight_classes=weight_classes,
                                        colors=colors,
                                        row=1,
                                        col=2,
                                        showlegend=False
                                        )
    fig = get_lift_plot_per_weightclass(fig,
                                        data=df_d,
                                        lift='Deadlift',
                                        weight_classes=weight_classes,
                                        colors=colors,
                                        row=1,
                                        col=3,
                                        showlegend=False
                                        )
    fig = get_lift_plot_per_weightclass(fig,
                                        data=df_t,
                                        lift='Total',
                                        weight_classes=weight_classes,
                                        colors=colors,
                                        row=1,
                                        col=4,
                                        showlegend=False
                                        )
    fig = get_lift_plot_per_weightclass(fig,
                                        data=df_w,
                                        lift='Wilks',
                                        weight_classes=weight_classes,
                                        colors=colors,
                                        row=1,
                                        col=5,
                                        showlegend=False
                                        )

    return fig
