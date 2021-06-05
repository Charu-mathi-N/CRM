from django.urls import path
from .views import AgentListView, AgentDetailsView, AgentCreateView, AgentUpdateView, agent_delete

app_name = 'agents'

urlpatterns = [
    path('', AgentListView.as_view(), name='agent_list'),
    path('<int:pk>/', AgentDetailsView.as_view(), name='agent_details'),
    path('create/', AgentCreateView.as_view(), name='agent_create'),
    path('<int:pk>/update', AgentUpdateView.as_view(), name='agent_update'),
    path('<int:pk>/delete', agent_delete, name='agent_delete'),
]
