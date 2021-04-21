import pandas as pd
import io
import ast
import plotly.graph_objs as go
from plotly.offline import plot
from plotly import tools
from core.shareplum_helper import get_data
from io import BytesIO
import urllib3
urllib3.disable_warnings()


team_slug = 'FinanceDevPatrol/'
folder_name = 'finance_data_analytics'

file_name1 = 'amzn_stock_data.csv'
chart_data1 = get_data(team_slug, folder_name, file_name1)
df1 = pd.read_csv(BytesIO(chart_data1))

file_name2 = 'amzn_tweepy_data.csv'
chart_data2 = get_data(team_slug, folder_name, file_name2)
df2 = pd.read_csv(BytesIO(chart_data2))

negative_sentiment = 0
neutral_sentiment = 0
positive_sentiment = 0
subjectivity_sentiment = 0
polarity1_sentiment = 0

for eachrow in df2['polarity']:
    eachrow_dict = ast.literal_eval(eachrow)
    for key,value in eachrow_dict.items():
        if key == 'neg':
            negative_sentiment +=value
        if key == 'neu':
            neutral_sentiment+=value
        if key == 'pos':
            positive_sentiment +=value
subjectivity_sentiment = sum(df2['Subjectivity'])
polarity1_sentiment = sum(df2['Polarity1'])
  
  
def fin_chart1():
    index, = (name for name in df1.columns if 'index' in name)
    for name in df1.columns:
        if '. adjusted close' in name:
            close = name
            break
        elif '. close' in name:
            close = name
    symbol='AMZN'
    timeframe = 'Time Series - Daily Adjusted -'
    data = go.Scatter(x=df1[index], y=df1[close], name=timeframe+'close($)')
    layout = go.Layout(title=f'{symbol} Stock {timeframe} Close($)')
    fig = go.Figure(data=data, layout=layout)
    plot_div = plot(fig, output_type='div', include_plotlyjs=False)
    return plot_div


def fin_chart2():
    index, = (name for name in df1.columns if 'index' in name)
    volume, = (name for name in df1.columns if '. volume' in name)
    symbol='AMZN'
    timeframe = 'Time Series - Daily Adjusted -'
    data = go.Scatter(x=df1[index], y=df1[volume], name=timeframe+'volume')
    layout = go.Layout(title=f'{symbol} Stock {timeframe} Volume')    
    fig = go.Figure(data=data, layout=layout)
    plot_div = plot(fig, output_type='div', include_plotlyjs=False)
    return plot_div
 

def fin_chart3():
    labels = ['Negative Sentiment','Positive Sentiment','Neutral Sentiment ']
    values = [negative_sentiment,positive_sentiment,neutral_sentiment]
    data = go.Pie(labels=labels, values=values,
                   hoverinfo='label+percent', textinfo='percent+label', 
                   textfont=dict(size=10),
                   marker=dict(colors=['#FEBFB3', '#E1396C', '#96D38C', '#D0F9B1'])
                 )
    layout = go.Layout(title='Twitter Sentiment Analysis - Oct 2020 to Present')
    fig = go.Figure(data=data, layout=layout)
    fig.update_traces(textposition='inside')
    plot_div = plot(fig, output_type='div', include_plotlyjs=False)
    return plot_div

	
def fin_chart4():
    labels = ['Subjectivity Sentiment','Polarity Sentiment']
    values = [subjectivity_sentiment,polarity1_sentiment]
    data = go.Pie(labels=labels, values=values)
    layout = go.Layout(title='Twitter Sentiment Analysis - Oct 2020 to Present')
    fig = go.Figure(data=data, layout=layout)
    plot_div = plot(fig, output_type='div', include_plotlyjs=False)
    return plot_div
