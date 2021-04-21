from django.urls import path
from . import views


urlpatterns = [
  path('', views.home, name='home'),
  path('about', views.about, name='about'), 
  path('signin', views.sign_in, name='signin'),
  path('signout', views.sign_out, name='signout'),  
  path('dashboard', views.dashboard, name='dashboard'),
  path('finance', views.finance, name='finance'), 
  path('manufacturing', views.manufacturing, name='manufacturing'), 
  path('retail', views.retail, name='retail'), 
  path('salesmarketing', views.salesmarketing, name='salesmarketing'),  
  path('misc', views.misc, name='misc'),     
  path('team', views.team, name='team'),    
  path('callback', views.callback, name='callback'),
]