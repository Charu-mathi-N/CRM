from django.urls import path
from .views import leads_details, leads_list, leads_create, lead_update, lead_delete

app_name = 'leads'

urlpatterns = [
    path('', leads_list, name='leads_list'),
    path('<int:pk>/', leads_details, name='leads_details'),
    path('create/', leads_create, name='leads_create'),
    path('<int:pk>/update', lead_update, name='leads_update'),
    path('<int:pk>/delete', lead_delete, name='leads_delete'),
]
