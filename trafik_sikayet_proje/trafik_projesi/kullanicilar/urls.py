from django.urls import path
from . import views

urlpatterns = [
    path('', views.settings, name='settings'), 
    path('account/', views.account_settings, name='account_settings'),  
    path('security/', views.security_settings, name='security_settings'),  
    path('notifications/', views.notification_settings, name='notification_settings'),
    path('privacy/', views.privacy_settings, name='privacy_settings'), 
    path('login/', views.login_view, name='login'),  
]

