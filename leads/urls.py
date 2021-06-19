from leads.forms import AssignAgentForm
from django.urls import path
from .views import AssignAgentView, CategoryDetailView, CategoryListView, LeadCategoryUpdatelView, LeadDetailsView, LeadListView, LeadDetailsView, LeadCreateView, LeadUpdateView, lead_delete
from django.urls import path

app_name = 'leads'

urlpatterns = [
    path('', LeadListView.as_view(), name='leads_list'),
    path('<int:pk>/', LeadDetailsView.as_view(), name='leads_details'),
    path('create/', LeadCreateView.as_view(), name='leads_create'),
    path('<int:pk>/update', LeadUpdateView.as_view(), name='leads_update'),
    path('<int:pk>/delete', lead_delete, name='leads_delete'),
    path('<int:pk>/assign/', AssignAgentView.as_view(), name='assign_agent'),
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category_details'),
    path('<int:pk>/category_update', LeadCategoryUpdatelView.as_view(), name='category_update'),
]