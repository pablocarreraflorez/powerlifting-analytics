# Imports
import pandas as pd
import plotly.express as px


# Functions
def get_weight_classes(federation, sex):
    """
    Get weight classes for a given sex and federation.

    :param str federation: federation to take weight classes from. 'IPF' or 'WRPF'.
    :param str sex: sex to take weight classes from. 'M' or 'F'.
    :return list bins:
    :return list labels:
    """
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
                              'Bodyweight',      # 'Bodyweight'
                              'WeightClass',     # 'WeightClassKg'
                              'Squat1',          # 'Squat1Kg'
                              'Squat2',          # 'Squat2Kg'
                              'Squat3',          # 'Squat3Kg'
                              'Squat4',          # 'Squat4Kg'
                              'SquatBest',       # 'Best3SquatKg'
                              'Bench1',          # 'Bench1Kg'
                              'Bench2',          # 'Bench2Kg'
                              'Bench3',          # 'Bench3Kg'
                              'Bench4',          # 'Bench4Kg'
                              'BenchBest',       # 'Best3BenchKg'
                              'Deadlift1',       # 'Deadlift1Kg'
                              'Deadlift2',       # 'Deadlift2Kg'
                              'Deadlift3',       # 'Deadlift3Kg'
                              'Deadlift4',       # 'Deadlift4Kg'
                              'DeadliftBest',    # 'Best3DeadliftKg'
                              'Total',           # 'TotalKg'
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
                              'Meet'               # 'MeetName'
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
                                'SquatBest',
                                'Bench1',
                                'Bench2',
                                'Bench3',
                                'BenchBest',
                                'Deadlift1',
                                'Deadlift2',
                                'Deadlift3',
                                'DeadliftBest',
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
                              'SquatBest': 'float',
                              'Bench1': 'float',
                              'Bench2': 'float',
                              'Bench3': 'float',
                              'BenchBest': 'float',
                              'Deadlift1': 'float',
                              'Deadlift2': 'float',
                              'Deadlift3': 'float',
                              'DeadliftBest': 'float',
                              'Total': 'float',
                              'Wilks': 'float'
                              },
                       parse_dates=['Date']
                       )

    # Perform some universal cleaning
    data = data.loc[data['Event'] == 'SBD']
    data = data.loc[data['Sex'] != 'Mx']
    data = data.loc[data['Equipment'].isin(['Raw', 'Wraps'])]

    # Drop null values
    data = data.dropna(subset=['SquatBest', 'BenchBest', 'DeadliftBest', 'Total'])

    return data


def clean_data(data, federation, equipment):
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
    if equipment == 'Raw':
        df = df.loc[df['Equipment'] == 'Raw']

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
    :return pandas.DataFrame df: data from n best lifts for weight class and sex
    """
    # Perform the filter and the groupings
    df = data[data['Sex'] == sex]\
        .sort_values(by=['WeightClass', 'Name', lift], ascending=False)\
        .groupby(['WeightClass', 'Name'], as_index=False).first()\
        .sort_values(by=['WeightClass', lift], ascending=False)\
        .groupby('WeightClass', as_index=False).head(n)

    return df


def plot_best_lifts_per_weightclass(data, lift, sex, federation, title):
    """

    :param pandas.DataFrame data: data with n best lifts for weight class and sex.
    :param str sex: sex to filter. 'M' or 'F'.
    :param str lift: lift to track.
    :param str federation: federation to take weight classes from. 'IPF' or 'WRPF'.
    :param str title: title for the figure.
    :return:
    """
    # Get weight classes
    _, weight_classes = get_weight_classes(federation=federation, sex=sex)

    # Make the figure
    fig = px.scatter(data,
                     x='Bodyweight',
                     y=lift,
                     color='WeightClass',
                     title=title,
                     hover_name='Name',
                     hover_data=['Meet', 'ParentFederation', 'Date'],
                     opacity=0.5,
                     category_orders={'WeightClass': weight_classes},
                     color_discrete_sequence=px.colors.qualitative.G10
                     )

    return fig
