from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from core.auth_helper import get_sign_in_url, get_token_from_code, store_token, store_user, remove_user_and_token, get_token
from core.msgraphapi_helper import get_user, get_team_members
from core.finance_util import fin_chart1, fin_chart2, fin_chart3, fin_chart4
from core.manufacturing_util import man_chart1, man_chart2, man_chart3, man_chart4
from core.retail_util import ret_chart1, ret_chart2, ret_chart3, ret_chart4, ret_chart5, ret_chart6, ret_chart7, ret_chart8, ret_chart9, ret_chart10, ret_chart11, ret_chart12, ret_chart13, ret_chart14
from core.salesmarketing_util import sm_chart1, sm_chart2, sm_chart3
import dateutil.parser
import requests
import datetime
import pytz


#Plugged in fake dashboard data for now ...
finance_dashboard = ['Gross Profit Margin (%)','Net Profit Margin (%)','Inventory Turnover Ratio', [5,50,100,[0,20,40,60,80,100]],[5,10,100,[0,20,40,60,80,100]],[2,5,10,[0,2,4,6,8,10]], 71, 14, 5.5, 'finance-border', 'finance-text']
manufacturing_dashboard = ['Back Order Rate (%)','Perfect Order Rate (%)','Units Per Transaction', [5,50,100,[0,20,40,60,80,100]],[5,10,100,[0,20,40,60,80,100]],[2,5,10,[0,2,4,6,8,10]], 12.10, 94.5, 5.3, 'manufacturing-border', 'manufacturing-text']
retail_dashboard = ['Avg Purchase Value (%)','Avg Transaction Value (%)','Conversion Rate (%)', [5,50,100,[0,20,40,60,80,100]],[5,50,100,[0,20,40,60,80,100]],[10,20,100,[0,20,40,60,80,100]], 67.55, 72.5, 25, 'retail-border', 'retail-text']
salesmarketing_dashboard = ['Sales Growth YTD (%)','Site Bounce Rate (%)', 'Sell-Through Rate (%)', [5,15,100,[0,20,40,60,80,100]],[5,15,100,[0,20,40,60,80,100]],[5,10,100,[0,20,40,60,80,100]], 32.7, 22.3, 13.48, 'salesmarketing-border', 'salesmarketing-text']

#Team charts...
finance_charts = [fin_chart1, fin_chart2, fin_chart3, fin_chart4]
manufacturing_charts = [man_chart1, man_chart2, man_chart3, man_chart4]
retail_charts = [ret_chart1, ret_chart2, ret_chart3, ret_chart4, ret_chart5, ret_chart6, ret_chart7, ret_chart8, ret_chart9, ret_chart10, ret_chart11, ret_chart12, ret_chart13, ret_chart14]
salesmarketing_charts = [sm_chart1, sm_chart2, sm_chart3]

#MS Graph API group IDs to obtain team list...
finance_id = '02d6954e-08bb-4c2e-a8b0-185562e48177'
manufacturing_id = 'efa0f638-aaae-452e-8f35-4366a09430eb'
retail_id = 'f2659784-eb13-41b6-9163-2fcc37288635'
salesmarketing_id = '943d9146-f560-4b5a-874d-d315dd2064f0'
executive_id = 'c2c2e9ef-966b-4168-9aa9-11a15bd60cbe'


def home(request):
    context = initialize_context(request)
    user = context['user']
    if request.user.is_authenticated or user['is_authenticated']==True:
        return HttpResponseRedirect('dashboard')
    else:  
        return render(request, 'core/home.html', context) 


def about(request):
    context = initialize_context(request)
    user = context['user']
    return render(request, 'core/about.html', context) 


def dashboard(request):
    context = initialize_context(request)
    token = get_token(request) 
    # Get user dept info and get charts based on this info
    dept = get_dept(request)
    group_type = get_group_type(dept)
    # Get current date & time
    curr_datetime = (datetime.datetime.now()).replace(tzinfo=pytz.utc)
    current_date_str = curr_datetime.strftime("%a, %b %d, %Y")    
    context['groupName'] = group_type
    context['currentDate'] = current_date_str  
    if group_type != 'Misc Group':
        if group_type == 'Executive Management':
            context['finance'] = finance_dashboard
            context['manufacturing'] = manufacturing_dashboard
            context['retail'] = retail_dashboard
            context['salesmarketing'] = salesmarketing_dashboard            
            return render(request, 'core/mgmt_dashboard.html', context)
        else:
            dept_dashboard = get_dashboard(dept)               
            context['dashtitle1'] = dept_dashboard[0]
            context['dashtitle2'] = dept_dashboard[1]
            context['dashtitle3'] = dept_dashboard[2]
            context['rangeset1'] = dept_dashboard[3]
            context['rangeset2'] = dept_dashboard[4]
            context['rangeset3'] = dept_dashboard[5]
            context['gauge1'] = dept_dashboard[6]
            context['gauge2'] = dept_dashboard[7]
            context['gauge3'] = dept_dashboard[8]
            context['borderStyle'] = dept_dashboard[9]
            context['textStyle'] = dept_dashboard[10]
    return render(request, 'core/dashboard.html', context)


def initialize_context(request):
    context = {}
    # Check for any errors in the session
    error = request.session.pop('flash_error', None)
    if error != None:
        context['errors'] = []
        context['errors'].append(error)
    # Check for user in the session and update authentication status
    context['user'] = request.session.get('user', {'is_authenticated': False})
    return context


def sign_in(request):
    # Get the sign-in URL
    sign_in_url, state = get_sign_in_url()
    # Save the expected state so we can validate in the callback
    request.session['auth_state'] = state
    # Redirect to the Azure sign-in page
    return HttpResponseRedirect(sign_in_url)


def callback(request):
    # Get the state saved in session
    expected_state = request.session.pop('auth_state', '')
    # Make the token request
    token = get_token_from_code(request.get_full_path(), expected_state)
    # Get the user's info
    user = get_user(token)
    # Save token and user
    store_token(request, token)
    store_user(request, user)
    return HttpResponseRedirect(reverse('dashboard'))


def sign_out(request):
    # Clear out the user and token
    remove_user_and_token(request)
    return HttpResponseRedirect(reverse('home'))


def team(request):
    context = initialize_context(request)
    token = get_token(request)  
    dept = get_dept(request)
    group_id = get_group_id(dept)
    team = get_team_members(token, group_id)  
    context['team'] = team['value']
    context['groupName'] = get_group_type(dept) 
    return render(request, 'core/team.html', context)    


def finance(request):
    context = initialize_context(request)
    token = get_token(request)   
    dept = get_dept(request)
    group_type = get_group_type(dept)
    context['groupName'] = group_type        
    context['plot1'] = finance_charts[0]
    context['plot2'] = finance_charts[1]
    context['plot3'] = finance_charts[2]
    context['plot4'] = finance_charts[3]  
    return render(request, 'core/finance_charts.html', context)


def manufacturing(request):
    context = initialize_context(request)
    token = get_token(request)
    dept = get_dept(request)
    group_type = get_group_type(dept)
    context['groupName'] = group_type 
    context['plot1'] = manufacturing_charts[0]
    context['plot2'] = manufacturing_charts[1]
    context['plot3'] = manufacturing_charts[2]
    context['plot4'] = manufacturing_charts[3]     
    return render(request, 'core/manufacturing_charts.html', context)


def retail(request):
    context = initialize_context(request)
    token = get_token(request)
    dept = get_dept(request)
    group_type = get_group_type(dept)
    context['groupName'] = group_type 
    context['plot1'] = retail_charts[0]
    context['plot2'] = retail_charts[1]
    context['plot3'] = retail_charts[2]
    context['plot4'] = retail_charts[3]
    context['plot5'] = retail_charts[4]
    context['plot6'] = retail_charts[5]
    context['plot7'] = retail_charts[6]
    context['plot8'] = retail_charts[7]
    context['plot9'] = retail_charts[8]
    context['plot10'] = retail_charts[9]
    context['plot11'] = retail_charts[10]
    context['plot12'] = retail_charts[11]
    context['plot13'] = retail_charts[12]
    context['plot14'] = retail_charts[13]     
    return render(request, 'core/retail_charts.html', context)
    
    
def salesmarketing(request):
    context = initialize_context(request)
    token = get_token(request)
    dept = get_dept(request)
    group_type = get_group_type(dept)
    context['groupName'] = group_type 
    context['plot1'] = salesmarketing_charts[0]
    context['plot2'] = salesmarketing_charts[1]
    context['plot3'] = salesmarketing_charts[2]    
    return render(request, 'core/salesmarketing_charts.html', context)    
    

def misc(request):
    context = initialize_context(request)
    token = get_token(request)
    dept = get_dept(request)
    group_type = get_group_type(dept)
    context['groupName'] = group_type 
    return render(request, 'core/misc_charts.html', context)
    

def get_dept(request):
    dept = request.session['user']['department']
    return dept
    

def get_dashboard(dept):
    dashboard = []
    if (dept == 'Sales') or (dept == 'Marketing') or (dept == 'Sales & Marketing'):
        dashboard = salesmarketing_dashboard
    elif dept == 'Retail':
        dashboard = retail_dashboard
    elif (dept == 'Manufacturing') or (dept == 'R&D'):
        dashboard = manufacturing_dashboard
    elif dept == 'Finance':
        dashboard = finance_dashboard
    elif dept == 'Executive Management':
        dashboard = executive_dashboard
    else:
        dashboard = None
    return dashboard

   
def get_group_id(dept):
    url = ''
    if (dept == 'Sales') or (dept == 'Marketing') or (dept == 'Sales & Marketing'):
        grp_id = salesmarketing_id
    elif dept == 'Retail':
        grp_id = retail_id
    elif (dept == 'Manufacturing') or (dept == 'R&D'):
        grp_id = manufacturing_id
    elif dept == 'Finance':
        grp_id = finance_id
    elif dept == 'Executive Management':
        grp_id = executive_id
    else:
        grp_id = None
    return grp_id
    
    
def get_group_type(dept):
    url = ''
    if (dept == 'Sales') or (dept == 'Marketing') or (dept == 'Sales & Marketing'):
        grp_type = 'Sales & Marketing Group'
    elif dept == 'Retail':
        grp_type = 'Retail Group'
    elif (dept == 'Manufacturing') or (dept == 'R&D'):
        grp_type = 'Manufacturing Group'
    elif dept == 'Finance':
        grp_type = 'Finance Group'
    elif dept == 'Executive Management':
        grp_type = 'Executive Management'
    else:
        grp_type = 'Misc Group'
    return grp_type