import data
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# currencies = ['USD', 'CAD']
currencies = ['USD']
connection_metrics = ['Exposure Usage', 'Exposure Limit']
connections = data.get_top10_connections()
connection_dates = data.get_conn_dates()
connection_data = data.get_connection_data()
line_shapes = {'Exposure Usage': 'vh', 'Exposure Limit': 'vh'}
lower_bounds = data.get_lower_bounds()
table_header_color = px.colors.qualitative.Plotly[2]

top_10_summary = go.Figure()

top_10_table = {}

for currency in currencies:
    top_10_data = data.get_top10_data(currency)
    top_10_table[currency] = go.Table(
        columnwidth=[3, 5, 12, 8, 5, 5, 5, 5, 5, 5, 5],
        header=dict(values=list(top_10_data.columns),
                    fill_color=table_header_color,
                    align='center'),
        cells=dict(values=[top_10_data['Rank'], top_10_data['Connection ID'], top_10_data['Connection Name'],
                           top_10_data['In/Common'], top_10_data['Exposure Usage'] / 1000000,
                           top_10_data['Exposure Limit'] / 1000000, top_10_data['% Utilized'],
                           top_10_data['% D/D'], top_10_data['Metric 1'] / 1000000,
                           top_10_data['Metric 2'] / 1000000, top_10_data['Metric 3'] / 1000000],
                   align=['center', 'right', 'left', 'center', 'right', 'right',
                          'right', 'right', 'right', 'right', 'right'],
                   format=['', '', '', '', ',.0f', ',.0f', ',.1%', ',.1%', ',.0f', ',.0f', ',.0f']),
        visible=currency == currencies[0])
    top_10_summary.add_trace(top_10_table[currency])

top_10_summary.update_layout(
    title='Top 10 Exposure Report',
    title_font_size=24,
    height=350,
    width=1570,
    autosize=True,
    margin=dict(b=1, pad=0),
    updatemenus=[
        dict(buttons=list([dict(label='USD', method='update', args=[{'visible': [True, False]}]),
                           dict(label='CAD', method='update', args=[{'visible': [False, True]}])]),
             direction='down',
             x=0,
             xanchor='left',
             y=1,
             yanchor='bottom')
    ]
)

connection_trend_line = go.Figure()

connection_traces = {}
for currency in currencies:
    connection_traces[currency] = []

for metric in connection_metrics:
    for connection in connections:
        connection_trend_line.add_scatter(x=connection_dates, y=connection_data[connection[0]][metric][currencies[0]],
                                          visible=connection[0] == connections[0][0], name=metric, connectgaps=True,
                                          line_shape=line_shapes[metric], hoverlabel=dict(namelength=-1))
        for currency in currencies:
            connection_traces[currency].append(connection_data[connection[0]][metric][currency])

connection_trend_line.add_scatter(x=connection_dates, y=lower_bounds[currencies[0]], name='Top 10 lower bound',
                                  connectgaps=True, line_shape='linear', hoverlabel=dict(namelength=-1))
for currency in currencies:
    connection_traces[currency].append(lower_bounds[currency])

connection_trend_line.update_layout(
    title='Connection-level Exposure Usage and Limit',
    xaxis_title='Date',
    yaxis_title='(USD)',
    yaxis_separatethousands=True,
    height=450,
    width=1570,
    autosize=True,
    margin=dict(b=1, pad=0),
    updatemenus=[
        dict(buttons=list([dict(args=[{'visible': list(pd.Series(connections) == connection) * 2 + [True]}],
                                label=connection[1],
                                method='update') for connection in connections]),
             direction='down',
             x=0.1,
             xanchor='left',
             y=1,
             yanchor='bottom'),
        dict(buttons=list([dict(label='USD',
                                method='update',
                                args=[{'y': connection_traces['USD']}, {'yaxis': {'title': '(USD)'}}]),
                           dict(label='CAD',
                                method='update',
                                args=[{'y': connection_traces['USD']}, {'yaxis': {'title': '(CAD)'}}])]),
             direction='down',
             x=0, xanchor='left', y=1,
             yanchor='bottom')])

figures = [top_10_summary, connection_trend_line]

for i in range(len(figures)):
    open('output.html', 'w' if i == 0 else 'a').write(figures[i].to_html(full_html=False, include_plotlyjs='cdn'))
