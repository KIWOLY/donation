from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('campaign/<int:pk>/', views.campaign_detail, name='campaign_detail'),
    path('donor/', views.donor_dashboard, name='donor_dashboard'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

]