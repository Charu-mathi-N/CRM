import logging
from django.views.generic.detail import DetailView
# from django.views.generic.edit import CreateView

from django.contrib import messages
from django.shortcuts import render, redirect, reverse
from .models import Lead, Agent, Category
from django.views import generic
from .forms import LeadModelForm, CustomUserCreationForm, AssignAgentForm, LeadCategoryUpdateForm
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

class LeadListView(LoginRequiredMixin, generic.ListView):
    template_name = "leads/lead_list.html"
    context_object_name = "leads"

    # def get_queryset(self):
    #     queryset = Lead.objects.all()
    #     if self.request.user.is_agent:
    #         queryset = Lead.objects.filter(agent__user=self.request.user)
    #     return queryset

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

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organisation
        if user.is_organisor:
            queryset = Lead.objects.filter(organisation=user.userprofile)
            print("Is organisor")
        else:
            queryset = Lead.objects.filter(organisation=user.agent.organisation)
            # filter for the agent that is logged in
            queryset = queryset.filter(agent__user=user)
        return queryset

# def leads_details(request, pk):
#     leads = Lead.objects.get(id = pk)
#     context = {
#         'leads': leads
#         }
#     return render(request, "leads/lead_details.html", context)


class LeadCreateView(OrganisorAndLoginRequiredMixin, generic.CreateView):
    template_name = "leads/lead_create.html" 
    form_class = LeadModelForm

    # def get_success_url(self):
    #     return reverse("leads:leads_list")

    def get_success_url(self):
        return reverse("leads:leads_list")

    def form_valid(self, form):
        lead = form.save(commit=False)
        lead.organisation = self.request.user.userprofile
        lead.save()
        messages.success(self.request, "You have successfully created a lead")
        return super(LeadCreateView, self).form_valid(form)


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

class AssignAgentView(OrganisorAndLoginRequiredMixin, generic.FormView):
    template_name = 'leads/assign_agent.html'
    form_class = AssignAgentForm

    def get_form_kwargs(self, **kwargs):
        kwargs = super(AssignAgentView, self).get_form_kwargs(**kwargs)
        kwargs.update({
            "request": self.request
        })
        return kwargs

    def get_success_url(self):
        return reverse("leads:leads_list")
    
    def form_valid(self, form):
        agent = form.cleaned_data["agent"]
        lead = Lead.objects.get(id=self.kwargs["pk"])
        lead.agent = agent
        lead.save()
        return super(AssignAgentView, self).form_valid(form)


class CategoryListView(LoginRequiredMixin, generic.ListView):
    template = 'leads/category_list.html'
    context_object_name = "category_list"

    def get_context_data(self, **kwargs):
        user = self.request.user
        if user.is_organisor:
            queryset = Lead.objects.filter(
                organisation=user.userprofile
        )
        else:
            queryset = Lead.objects.filter(
                organisation=user.agent.organisation
        )
        context = super(CategoryListView, self).get_context_data(**kwargs)
        context.update({
            "unassinged_lead_count" : queryset.filter(category__isnull=True).count()
        })
        return context

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organisation
        if user.is_organisor:
            queryset = Category.objects.filter(
                organisation=user.userprofile
            )
        else:
            queryset = Category.objects.filter(
                organisation=user.agent.organisation
            )
        return queryset

class CategoryDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "leads/category_details.html"
    context_object_name = "category"

    # def get_context_data(self, **kwargs):
    #     context = super(CategoryDetailView, self).get_context_data(**kwargs)

    #     # qs = Lead.objects.filter(category=self.get_object())
    #     leads = self.get_object().leads.all()

    #     context.update({
    #         "leads" : leads
    #     })
    #     return context
    
    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organisation
        if user.is_organisor:
            queryset = Category.objects.filter(
                organisation=user.userprofile
            )
        else:
            queryset = Category.objects.filter(
                organisation=user.agent.organisation
            )
        return queryset

class LeadCategoryUpdatelView(OrganisorAndLoginRequiredMixin, generic.UpdateView):
    template_name = "leads/category_update.html"
    form_class = LeadCategoryUpdateForm

    def get_success_url(self):
        return reverse("leads:category_list")

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organisation
        if user.is_organisor:
            queryset = Lead.objects.filter(organisation=user.userprofile)
            print("Is organisor")
        else:
            queryset = Lead.objects.filter(organisation=user.agent.organisation)
            # filter for the agent that is logged in
            queryset = queryset.filter(agent__user=user)
        return queryset

