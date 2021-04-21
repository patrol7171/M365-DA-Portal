import pandas as pd
import io
import plotly.graph_objs as go
from plotly.offline import plot
from plotly import tools
from plotly.subplots import make_subplots
from core.shareplum_helper import get_data
from io import BytesIO
import urllib3
urllib3.disable_warnings()


team_slug = 'SalesMarketingDevPatrol/'
folder_name = 'sales&marketing_data_analytics'
file_name = 'customer_data.csv'
chart_data = get_data(team_slug, folder_name, file_name)
df = pd.read_csv(BytesIO(chart_data))

    
def sm_chart1():
    fig = make_subplots(rows=1, cols=3)
    fig.add_trace(
        go.Scatter(x=df['Administrative'],y=df['Administrative_Duration'],mode='markers'),
        row=1,
        col=1
    )
    fig.add_trace(
        go.Scatter(x=df['Informational'],y=df['Informational_Duration'], mode='markers'),
        row=1,
        col=2
    )
    fig.add_trace(
        go.Scatter(x=df['ProductRelated'],y=df['ProductRelated_Duration'],mode='markers'),
        row=1,
        col=3
    )
    fig.update_xaxes(title_text="Administrative", row=1, col=1)
    fig.update_xaxes(title_text="Informational", row=1, col=2)
    fig.update_xaxes(title_text="Product Related", row=1, col=3)
    fig.update_yaxes(title_text="Duration", row=1, col=1)
    fig.update_layout(title_text="Duration of Pages Based On Type",showlegend=False)
    plot_div = plot(fig, output_type='div', include_plotlyjs=False)
    return plot_div


def sm_chart2():
    fig=go.Figure()
    fig.add_trace(go.Box(
        x=df['VisitorType'],
        y=df['ExitRates'],
        name='Visitor Type',
        marker_color='#FF851B'
    ))
    fig.update_layout(title_text='Visitor Type vs Exit Rates',boxmode='group')
    plot_div = plot(fig, output_type='div', include_plotlyjs=False)
    return plot_div
 

def sm_chart3():
    corr = df.corr()
    trace = go.Heatmap(z=corr.values,x=corr.index.values,y=corr.columns.values)
    data=[trace]
    layout = go.Layout(title='Correlation Map')
    fig = go.Figure(data=data,layout=layout)
    plot_div = plot(fig, output_type='div', include_plotlyjs=False)
    return plot_div

