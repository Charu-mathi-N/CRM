import logging
from django.views.generic.detail import DetailView
# from django.views.generic.edit import CreateView

from django.shortcuts import render, redirect, reverse
from .models import Lead, Agent
from django.views import generic
from .forms import LeadModelForm, CustomUserCreationForm
from django.views.generic import ListView, CreateView, UpdateView

from django.urls import reverse

from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from .mixins import OrganisorAndLoginRequiredMixin

# Create your views here.

logger = logging.getLogger(__name__)

#Authentication
class SignupView(generic.CreateView):
    template_name = "registration/signup.html"
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse("leads:leads_list")

class LandingPageView(generic.TemplateView):
    template_name = "landing.html"

class LeadListView(generic.ListView):
    template_name = "leads/lead_list.html"
    context_object_name = "leads"
    queryset = Lead.objects.all()

# def leads_list(request):
#     leads = Lead.objects.all()
#     context = {
#         'leads': leads
#         }
#     return render(request, "leads/lead_list.html", context)


class LeadDetailsView(LoginRequiredMixin, generic.DetailView):
    template_name = "leads/lead_details.html"
    queryset = Lead.objects.all()
    context_object_name = "leads"



# def leads_details(request, pk):
#     leads = Lead.objects.get(id = pk)
#     context = {
#         'leads': leads
#         }
#     return render(request, "leads/lead_details.html", context)


class LeadCreateView(OrganisorAndLoginRequiredMixin, generic.CreateView):
    template_name = "leads/lead_create.html" 
    form_class = LeadModelForm

    def get_success_url(self):
        return reverse("leads:leads_list")

# def leads_create(request):
#     form = LeadModelForm()
#     if(request.method == "POST"):
#         print("All good")
#         form = LeadModelForm(request.POST)
#         if(form.is_valid()):
#             print("Valid data")
#             print(form.cleaned_data)
#             form.save()
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
    #         print("Lead created")
    #         return redirect('/leads')
            
    # context = {
    #     'forms': LeadModelForm()
    #     }
    # return render(request, "leads/lead_create.html", context)


class LeadUpdateView(OrganisorAndLoginRequiredMixin, generic.UpdateView):
    template_name = "leads/lead_update.html"
    queryset = Lead.objects.all()
    form_class = LeadModelForm

    def get_success_url(self):
        return reverse("leads:leads_list")

 
# def lead_update(request, pk):
#     lead = Lead.objects.get(id=pk)
#     form = LeadModelForm(instance=lead)
#     if(request.method == "POST"):
#         print("All good")
#         form = LeadModelForm(request.POST)
#         if(form.is_valid()):
#             print("Valid Update")
#             print(form.cleaned_data)
#             form.save()
#     context = {
#         'forms': LeadModelForm()
#         }

#     return render(request, "leads/lead_update.html", context)

def lead_delete(request, pk):
    lead = Lead.objects.get(id=pk)
    lead.delete()
    return redirect('/leads')