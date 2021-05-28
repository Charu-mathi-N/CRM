from django.urls import path
from .views import  LeadDetailsView, LeadListView, LeadDetailsView, LeadCreateView, LeadUpdateView, lead_delete, SignupView
from django.contrib.auth.views import (
    LoginView,
    LogoutView, 
    PasswordResetView, 
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)
from django.urls import path
# from django.contrib.auth import views as auth_views
# from django.contrib.auth import 

app_name = 'leads'

urlpatterns = [
    path('', LeadListView.as_view(), name='leads_list'),
    path('<int:pk>/', LeadDetailsView.as_view(), name='leads_details'),
    path('create/', LeadCreateView.as_view(), name='leads_create'),
    path('<int:pk>/update', LeadUpdateView.as_view(), name='leads_update'),
    path('<int:pk>/delete', lead_delete, name='leads_delete'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('reset-password/', PasswordResetView.as_view(), name='reset-password'),
    path('password-reset-done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset-complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
