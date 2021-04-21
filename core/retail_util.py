import pandas as pd
import io
import plotly.graph_objs as go
from plotly.offline import plot
from plotly import tools
from core.shareplum_helper import get_data
from io import BytesIO
import urllib3
urllib3.disable_warnings()


team_slug = 'RetailDevPatrol/'
folder_name = 'retail_data_analytics'

file_name1 = 'returned_orders_per_category.csv'
chart_data1 = get_data(team_slug, folder_name, file_name1)
df1 = pd.read_csv(BytesIO(chart_data1))  

file_name2 = 'successful_orders_per_category.csv'
chart_data2 = get_data(team_slug, folder_name, file_name2)
df2 = pd.read_csv(BytesIO(chart_data2)) 
  
    
def ret_chart1():
    orders = df1.groupby(by=['Store_type'], as_index = False)['Qty'].count()
    trace = go.Pie(labels = orders['Store_type'], values = orders['Qty'])
    data = [trace]
    layout = go.Layout(title='Total # of Returned Orders Per Store Category')       
    fig = go.Figure(data=data, layout=layout)
    plot_div = plot(fig, output_type='div', include_plotlyjs=False)
    return plot_div


def ret_chart2():
    category = df1.groupby(by=['prod_cat'], as_index = False)['Qty'].count()
    data = go.Bar(x=category['prod_cat'],y=category['Qty'])
    layout = go.Layout(title='Total # of Returned Orders Per Product Category')   
    fig = go.Figure(data=data, layout=layout)
    plot_div = plot(fig, output_type='div', include_plotlyjs=False)
    return plot_div
 

def ret_chart3():
    city = df1.groupby(by=['city_code'], as_index = False)['Qty'].count()
    data = go.Bar(x=city['city_code'],y=city['Qty'],marker={'color':city['Qty'],'colorscale': 'Oryel'})
    layout = go.Layout(title='Total # of Returned Orders Per City')
    fig = go.Figure(data=data, layout=layout)
    fig.update_xaxes(type='category',title_text='City Code')
    plot_div = plot(fig, output_type='div', include_plotlyjs=False)
    return plot_div

	
def ret_chart4():
    order_year = df1.groupby(by=['year'], as_index = False)['Qty'].count()       
    data = go.Bar(x=order_year['year'],y=order_year['Qty'],marker_color='red')
    layout = go.Layout(title='Returned Orders Per Year')
    fig = go.Figure(data=data, layout=layout)
    fig.update_xaxes(type='category',title_text='Year')
    plot_div = plot(fig, output_type='div', include_plotlyjs=False)
    return plot_div
	

def ret_chart5():
    sales = df1.groupby(by=['year'], as_index = False)['total_amt'].sum()
    data = go.Bar(x=sales['year'],y=sales['total_amt'],marker_color='red')
    layout = go.Layout(title='Revenue Lost Due To Returns')
    fig = go.Figure(data=data, layout=layout)
    fig.update_xaxes(type='category',title_text='Year')
    plot_div = plot(fig, output_type='div', include_plotlyjs=False)
    return plot_div


def ret_chart6():
    orders = df2.groupby(by=['Store_type'], as_index = False)['Qty'].count()
    trace = go.Pie(labels=orders['Store_type'], values=orders['Qty'])
    data = [trace]
    layout = go.Layout(title='Total # of Successful Orders Per Store Category')
    fig = go.Figure(data=data, layout=layout)
    plot_div = plot(fig, output_type='div', include_plotlyjs=False)
    return plot_div 


def ret_chart7():
    category = df2.groupby(by=['prod_cat'], as_index = False)['Qty'].count()
    data = go.Bar(x=category['prod_cat'],y=category['Qty'],marker={'color':category['Qty'],'colorscale': 'Purp'})
    layout = go.Layout(title='Total # of Successful Orders Per Product Category')
    fig = go.Figure(data=data, layout=layout)
    plot_div = plot(fig, output_type='div', include_plotlyjs=False)
    return plot_div


def ret_chart8():
    subcategory = df2.groupby(by=['prod_subcat'], as_index = False)['total_amt'].sum()        
    data = go.Bar(x=subcategory['total_amt'],y=subcategory['prod_subcat'],orientation='h')
    layout = go.Layout(title='Amount Spent Per Subcategories')
    fig = go.Figure(data=data, layout=layout)
    fig.update_xaxes(title_text='Amount Spent')
    plot_div = plot(fig, output_type='div', include_plotlyjs=False)
    return plot_div


def ret_chart9():
    city = df2.groupby(by=['city_code'], as_index = False)['Qty'].count()
    data = go.Bar(x=city['city_code'],y=city['Qty'],marker={'color':city['Qty'],'colorscale': 'Tealgrn'})
    layout = go.Layout(title='Total # of Successful Orders Per City')
    fig = go.Figure(data=data, layout=layout)
    fig.update_xaxes(type='category',title_text='City Code')
    plot_div = plot(fig, output_type='div', include_plotlyjs=False)
    return plot_div    


def ret_chart10():
    order_year = df2.groupby(by=['year'], as_index = False)['Qty'].count()        
    data = go.Bar(x=order_year['year'],y=order_year['Qty'], marker_color='green')
    layout = go.Layout(title='Order Quantity Per Year')
    fig = go.Figure(data=data, layout=layout)
    fig.update_xaxes(type='category',title_text='Year')
    plot_div = plot(fig, output_type='div', include_plotlyjs=False)
    return plot_div


def ret_chart11():
    sales = df2.groupby(by=['year'], as_index = False)['total_amt'].sum()
    data = go.Bar(x=sales['year'],y=sales['total_amt'],marker_color='green')
    layout = go.Layout(title='Successful Orders - Revenue Generated')
    fig = go.Figure(data=data, layout=layout)
    fig.update_xaxes(type='category',title_text='Year')
    plot_div = plot(fig, output_type='div', include_plotlyjs=False)
    return plot_div
    
    
def ret_chart12():
    category_by_gender = df2.groupby(['Gender','prod_cat'], as_index=False)['total_amt'].sum()
    catF= category_by_gender[category_by_gender.Gender == 'F']
    catM = category_by_gender[category_by_gender.Gender == 'M']
    trace1 = go.Bar(x = catF['prod_cat'],y = catF['total_amt'],name = 'Female')
    trace2 = go.Bar(x = catM['prod_cat'],y = catM['total_amt'],name = 'Male')
    data = [trace1, trace2]
    layout = go.Layout(barmode = 'group',title='Successful Orders Per Product Category By Gender')
    fig = go.Figure(data = data, layout = layout)
    plot_div = plot(fig, output_type='div', include_plotlyjs=False)
    return plot_div


def ret_chart13():
    spend_per_category = df2.groupby(['age_category','prod_cat'])['total_amt'].sum().reset_index()
    age_group1 = spend_per_category[spend_per_category.age_category == '24-29']
    age_group2 = spend_per_category[spend_per_category.age_category == '30-39']
    age_group3 = spend_per_category[spend_per_category.age_category == '40-50']
    trace1 = go.Bar(x = age_group1['prod_cat'],y = age_group1['total_amt'],name = 'Ages 24-29')
    trace2 = go.Bar(x = age_group2['prod_cat'],y = age_group2['total_amt'],name = 'Ages 30-39')
    trace3 = go.Bar(x = age_group3['prod_cat'],y = age_group3['total_amt'],name = 'Ages 40-50')
    data = [trace1, trace2, trace3]
    layout = go.Layout(barmode = 'group',title='Successful Orders Per Product Category By Age Group')
    fig = go.Figure(data = data, layout = layout)
    plot_div = plot(fig, output_type='div', include_plotlyjs=False)
    return plot_div


def ret_chart14():
    sale_by_month = df2.groupby(['month','prod_cat'])['Qty'].count().reset_index()
    
    mnth1 = sale_by_month[sale_by_month.month == 1]
    mnth2 = sale_by_month[sale_by_month.month == 2]
    mnth3 = sale_by_month[sale_by_month.month == 3]
    mnth4 = sale_by_month[sale_by_month.month == 4]
    mnth5 = sale_by_month[sale_by_month.month == 5]
    mnth6 = sale_by_month[sale_by_month.month == 6]
    mnth7 = sale_by_month[sale_by_month.month == 7]
    mnth8 = sale_by_month[sale_by_month.month == 8]
    mnth9 = sale_by_month[sale_by_month.month == 9]
    mnth10 = sale_by_month[sale_by_month.month == 10]
    mnth11 = sale_by_month[sale_by_month.month == 11]
    mnth12 = sale_by_month[sale_by_month.month == 12]
    
    trace1 = go.Bar(x = mnth1['prod_cat'],y = mnth1['Qty'],name = 'Jan')
    trace2 = go.Bar(x = mnth2['prod_cat'],y = mnth2['Qty'],name = 'Feb')
    trace3 = go.Bar(x = mnth3['prod_cat'],y = mnth3['Qty'],name = 'Mar')
    trace4 = go.Bar(x = mnth4['prod_cat'],y = mnth4['Qty'],name = 'Apr')
    trace5 = go.Bar(x = mnth5['prod_cat'],y = mnth5['Qty'],name = 'May')
    trace6 = go.Bar(x = mnth6['prod_cat'],y = mnth6['Qty'],name = 'Jun')
    trace7 = go.Bar(x = mnth7['prod_cat'],y = mnth7['Qty'],name = 'Jul')
    trace8 = go.Bar(x = mnth8['prod_cat'],y = mnth8['Qty'],name = 'Aug')
    trace9 = go.Bar(x = mnth9['prod_cat'],y = mnth9['Qty'],name = 'Sep')
    trace10 = go.Bar(x = mnth10['prod_cat'],y = mnth10['Qty'],name = 'Oct',marker=dict(color='#e7f736'))
    trace11 = go.Bar(x = mnth11['prod_cat'],y = mnth11['Qty'],name = 'Nov',marker=dict(color='#632fa3'))
    trace12 = go.Bar(x = mnth12['prod_cat'],y = mnth12['Qty'],name = 'Dec',marker=dict(color='salmon'))

    data = [trace1,trace2,trace3,trace4,trace5,trace6,trace7,trace8,trace9,trace10,trace11,trace12]
    layout = go.Layout(barmode = 'stack',title='Successful Orders Per Product Category By Month')
    fig = go.Figure(data = data, layout = layout)
    plot_div = plot(fig, output_type='div', include_plotlyjs=False)
    return plot_div