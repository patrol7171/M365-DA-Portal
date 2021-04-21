import pandas as pd
import io
import plotly.graph_objs as go
from plotly.offline import plot
from plotly import tools
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from core.shareplum_helper import get_data
from io import BytesIO
import urllib3
urllib3.disable_warnings()


team_slug = 'ManufacturingDevPatrol/'
folder_name = 'manufacturing_data_analytics'
file_name = 'EconomiesOfScale.csv'
chart_data = get_data(team_slug, folder_name, file_name)
df = pd.read_csv(BytesIO(chart_data))
X_train, X_test, y_train, y_test = train_test_split(df['Number of Units'],df['Manufacturing Cost'],test_size = 0.3,random_state=42)


def man_chart1():
    corr = df.corr()
    trace = go.Heatmap(z=corr.values,x=corr.index.values,y=corr.columns.values)
    data = [trace]
    layout = go.Layout(title='Correlation Matrix')
    fig = go.Figure(data=data,layout=layout)
    plot_div = plot(fig, output_type='div', include_plotlyjs=False)
    return plot_div


def man_chart2():
    trace = go.Scatter(x=df['Number of Units'],y=df['Manufacturing Cost'],mode='markers',marker=dict(color='brown'))
    data=[trace]
    layout = go.Layout(title='Manufacturing Cost vs. Number of Units')
    fig = go.Figure(data=data,layout=layout)
    fig.update_xaxes(title_text='Manufacturing Cost')
    fig.update_yaxes(title_text='Number of Units')
    plot_div = plot(fig, output_type='div', include_plotlyjs=False)
    return plot_div
 

def man_chart3():
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=X_train,y=y_train,name='Training Data',mode='markers',marker=dict(color='blue')))
    fig.add_trace(go.Scatter(x=X_test,y=y_test,name='Test Data',mode='markers',marker=dict(color='red')))
    fig.update_layout(title='Manufacturing Cost - Test vs. Train')
    fig.update_layout(legend=dict(orientation="h", yanchor="top"))
    plot_div = plot(fig, output_type='div', include_plotlyjs=False)
    return plot_div


def man_chart4():
    reg = LinearRegression()
    reg.fit(X_train.values.reshape(-1,1), y_train.values)
    prediction = reg.predict(X_test.values.reshape(-1,1))
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=X_test,y=prediction,name='Linear Regression',mode='lines',marker=dict(color='salmon')))
    fig.add_trace(go.Scatter(x=X_test,y=y_test,name='Actual Test Data',mode='markers',marker=dict(color='teal')))
    fig.update_layout(title='Manufacturing Cost - Linear Regression')
    fig.update_layout(legend=dict(orientation="h", yanchor="top"))
    plot_div = plot(fig, output_type='div', include_plotlyjs=False)
    return plot_div