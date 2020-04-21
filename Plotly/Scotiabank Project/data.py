import numpy as np
import pandas as pd

df_connection_all = pd.read_excel('connections.xlsx')


# df_entity_all = pd.read_excel('entities.xlsx')
# df_ig_all = pd.read_excel('ig.xlsx')


def get_conn_dates():
    return sorted(list(set(df_connection_all['Date'])), reverse=True)


def get_top10_connections():
    df = df_connection_all[(df_connection_all['Currency'] == 'USD') & (df_connection_all['Date'] == valuation_date) & (
            df_connection_all['Rank'] <= 10)][['Connection ID', 'Connection Name']]
    return [(list(df['Connection ID'])[i], list(df['Connection Name'])[i]) for i in range(10)]


def get_top10_data(currency):
    metrics = ['Rank', 'Connection ID', 'Connection Name', 'In/Common', 'Exposure Usage', 'Exposure Limit',
               '% Utilized', 'Metric 1', 'Metric 2', 'Metric 3']
    df = df_connection_all[
        (df_connection_all['Currency'] == currency) & (df_connection_all['Date'] == valuation_date) & (
                df_connection_all['Rank'] <= 10)][metrics]
    prev_day_exposure = \
        df_connection_all[(df_connection_all['Currency'] == currency) & (df_connection_all['Date'] == reference_date)][
            ['Connection ID', 'Exposure Usage']]
    df = df.merge(prev_day_exposure, 'left', 'Connection ID', suffixes=['', ' Prev'])
    df['% D/D'] = [list(df['Exposure Usage'])[i] / list(df['Exposure Usage Prev'])[i] - 1 if
                   list(df['Exposure Usage Prev'])[i] > 0 else 1 for i in range(10)]
    metrics = ['Rank', 'Connection ID', 'Connection Name', 'In/Common', 'Exposure Usage', 'Exposure Limit',
               '% Utilized', '% D/D', 'Metric 1', 'Metric 2', 'Metric 3']
    return df[metrics]


def get_connection_metric_data(connection_id, metric, currency):
    return list(df_connection_all[(df_connection_all['Currency'] == currency) & (
            df_connection_all['Connection ID'] == connection_id)][metric])


def get_entity_metric_data(entity_id, metric, currency):
    return list(
        df_entity_all[(df_entity_all['Currency'] == currency) & (df_entity_all['Entity ID'] == entity_id)][metric])


def get_connection_data():
    connection_data = {}
    metrics = ['Exposure Usage', 'Exposure Limit']
    for connection in connections:
        connection_data[connection[0]] = {}
        for metric in metrics:
            connection_data[connection[0]][metric] = {}
            for currency in currencies:
                connection_data[connection[0]][metric][currency] = \
                    get_connection_metric_data(connection[0], metric, currency)
    return connection_data


def get_lower_bounds():
    lower_bounds = {}
    for currency in currencies:
        lower_bounds[currency] = \
            list(df_connection_all[(df_connection_all['Rank'] == 1) & (df_connection_all['Currency'] == currency)][
                     'Top 10 Lower Bound'])
    return lower_bounds


valuation_date = get_conn_dates()[0]
reference_date = get_conn_dates()[1]
currencies = ['USD', 'CAD']
connections = get_top10_connections()
