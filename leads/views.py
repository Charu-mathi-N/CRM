import logging
from django import contrib
from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView

from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Lead, Agent
from .forms import LeadModelForm
from django.contrib import messages
from django.core.mail import send_mail

from django.urls import reverse

from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import (
    LeadForm, 
    LeadModelForm, 
    CustomUserCreationForm
)

# Create your views here.

logger = logging.getLogger(__name__)


#Authentication
class SignupView(generic.CreateView):
    template_name = "registration/signup.html"
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse("leads:leads_list")

class LandingPageView(generic.TemplateView):
    template_name = "leads/landing.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("dashboard")
        return super().dispatch(request, *args, **kwargs)

class LeadListView(LoginRequiredMixin, generic.ListView):
    template_name = "leads/lead_list.html"
    context_object_name = "leads"

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organisation
        if user.is_organisor:
            queryset = Lead.objects.filter(
                organisation=user.userprofile, 
                agent__isnull=False
            )
        else:
            queryset = Lead.objects.filter(
                organisation=user.agent.organisation, 
                agent__isnull=False
            )
            # filter for the agent that is logged in
            queryset = queryset.filter(agent__user=user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(LeadListView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_organisor:
            queryset = Lead.objects.filter(
                organisation=user.userprofile, 
                agent__isnull=True
            )
            context.update({
                "unassigned_leads": queryset
            })
        return context

def leads_list(request):
    leads = Lead.objects.all()
    context = {
        'leads': leads
        }
    return render(request, "leads/lead_list.html", context)

def leads_details(request, pk):
    leads = Lead.objects.get(id = pk)
    context = {
        'leads': leads
        }
    return render(request, "leads/lead_details.html", context)

def leads_create(request):
    form = LeadModelForm()
    if(request.method == "POST"):
        print("All good")
        form = LeadModelForm(request.POST)
        if(form.is_valid()):
            print("Valid data")
            print(form.cleaned_data)
            form.save()
            #Alternate if LeadModelForm was not created

            # first_name = form.cleaned_data['first_name']
            # last_name = form.cleaned_data['last_name']
            # age = form.cleaned_data['age']
            # agent = Agent.objects.first()
            # Lead.objects.create(
            #     first_name = first_name,
            #     last_name = last_name,
            #     age = age,
            #     agent = agent
            # )
            print("Lead created")
            return redirect('/leads')
            
    context = {
        'forms': LeadModelForm()
        }
    return render(request, "leads/lead_create.html", context)

def lead_update(request, pk):
    lead = Lead.objects.get(id=pk)
    form = LeadModelForm(instance=lead)
    if(request.method == "POST"):
        print("All good")
        form = LeadModelForm(request.POST)
        if(form.is_valid()):
            print("Valid Update")
            print(form.cleaned_data)
            form.save()
    context = {
        'forms': LeadModelForm()
        }

    return render(request, "leads/lead_update.html", context)

def lead_delete(request, pk):
    lead = Lead.objects.get(id=pk)
    lead.delete()
    return redirect('/leads')