import random

from django.core.mail import send_mail
from django.views import generic
from django.views.generic.detail import DetailView
from django.shortcuts import redirect
from .forms import AgentModelForm
from leads.models import Agent
from django.views.generic import ListView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
# from .mixins import OrganisorAndLoginRequiredMixin

from django.urls import reverse


class AgentListView(LoginRequiredMixin, generic.ListView):
    template_name = "agents/agent_list.html"
    
    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)


class AgentCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = "agents/agent_create.html"
    form_class = AgentModelForm

    def get_success_url(self):
        return reverse("agents:agent_list")

    # def form_valid(self, form):
    #     user = form.save(commit=False)
    #     user.is_agent = True
    #     user.is_organisor = False
    #     user.set_password(f"{random.randint(0, 1000000)}")
    #     user.save()
    #     Agent.objects.create(
    #         user=user,
    #         organisation=self.request.user.userprofile
    #     )
    #     send_mail(
    #         subject="You are invited to be an agent",
    #         message="You were added as an agent on DJCRM. Please come login to start working.",
    #         from_email="admin@test.com",
    #         recipient_list=[user.email]
    #     )
    #     return super(AgentCreateView, self).form_valid(form)


class AgentDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "agents/agent_detail.html"
    context_object_name = "agent"

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)


class AgentUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "agents/agent_update.html"
    form_class = AgentModelForm

    def get_success_url(self):
        return reverse("agents:agent_list")

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)


class AgentDeleteView(LoginRequiredMixin, generic.DeleteView):
    template_name = "agents/agent_delete.html"
    context_object_name = "agent"

    def get_success_url(self):
        return reverse("agents:agent_list")

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)

# # Create your views here.
# class AgentListView(OrganisorAndLoginRequiredMixin, generic.ListView):
#     template_name = "agents/agent_list.html"
    
#     def get_queryset(self):
#         organisation = self.request.user.userprofile
#         return Agent.objects.filter(organisation=organisation)


# class AgentDetailsView(LoginRequiredMixin, generic.DetailView):
#     template_name = "agents/agents_details.html"
#     queryset = Agent.objects.all()
#     context_object_name = "agents"


# class AgentCreateView(LoginRequiredMixin, generic.CreateView):
#     template_name = "agents/agents_create.html" 
#     form_class = LeadModelForm

#     def get_success_url(self):
#         return reverse("agents:leads_list")


# class AgentUpdateView(LoginRequiredMixin, generic.UpdateView):
#     template_name = "agents/lead_update.html"
#     queryset = Agent.objects.all()
#     form_class = AgentModelForm

#     def get_success_url(self):
#         return reverse("agents:agents_list")

 
# def agent_delete(request, pk):
#     Agent = Agent.objects.get(id=pk)
#     Agent.delete()
#     return redirect('/agents')