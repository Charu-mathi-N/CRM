from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Lead, Agent
from .forms import LeadModelForm

# Create your views here.

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