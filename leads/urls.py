from leads.forms import AssignAgentForm
from django.urls import path
from .views import  AssignAgentView, LeadDetailsView, LeadListView, LeadDetailsView, LeadCreateView, LeadUpdateView, lead_delete, AssignAgentView
from django.urls import path

app_name = 'leads'

urlpatterns = [
    path('', LeadListView.as_view(), name='leads_list'),
    path('<int:pk>/', LeadDetailsView.as_view(), name='leads_details'),
    path('create/', LeadCreateView.as_view(), name='leads_create'),
    path('<int:pk>/update', LeadUpdateView.as_view(), name='leads_update'),
    path('<int:pk>/delete', lead_delete, name='leads_delete'),
    path('<int:pk>/assign', AssignAgentView.as_view, name='assign_agent'),
]
