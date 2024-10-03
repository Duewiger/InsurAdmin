from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models.query import QuerySet
from django.db.models import Q
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Insurance
from .forms import InsuranceChangeForm, InsuranceForm



class InsuranceCreationView(
    LoginRequiredMixin, 
    PermissionRequiredMixin,  
    CreateView):
    model = Insurance
    form_class = InsuranceForm
    template_name = "insurances/insurance_creation.html"
    permission_required = "insurances.special_status"
    login_url = "account_login"
    success_url = reverse_lazy("insurance_list")
    
    def form_valid(self, form):
        form.instance.customer = self.request.user
        return super().form_valid(form)



class InsuranceListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Insurance
    context_object_name = "insurance_list"
    template_name = "insurances/insurance_list.html"
    login_url = "account_login"
    # # Signals in Django für permissions verwenden zum automatischen setzen
    permission_required = "insurances.special_status"
    
    def get_queryset(self):
        return Insurance.objects.filter(customer=self.request.user)
    
    
    
class InsuranceDetailView(
        LoginRequiredMixin, 
        PermissionRequiredMixin, 
        DetailView):
    model = Insurance
    context_object_name = "insurance"
    template_name = "insurances/insurance_detail.html"
    login_url = "account_login"
    # # Signals in Django für permissions verwenden zum automatischen setzen
    permission_required = "insurances.special_status"
    
    def get_queryset(self):
        return Insurance.objects.filter(customer=self.request.user)



class InsuranceEditView(LoginRequiredMixin, UpdateView):
    model = Insurance
    form_class = InsuranceChangeForm
    template_name = "insurances/insurance_edit.html"
    login_url = "account_login"
    success_url = reverse_lazy("insurance_list")
    permission_required = "insurances.special_status"
    
    def form_valid(self, form):
        form.instance.customer = self.request.user
        return super().form_valid(form)
    
    
    
class InsuranceDeleteView(LoginRequiredMixin, DeleteView):
    model = Insurance
    template_name = "insurances/insurance_delete.html"
    success_url = reverse_lazy("insurance_list")
    login_url = "account_login"
    permission_required = "insurances.special_status"
    
    def get_queryset(self):
        return Insurance.objects.filter(customer=self.request.user)
    
    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(self.request, "Versicherung erfolgreich gelöscht.")
        return response
    
    
class SearchResultsView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Insurance
    context_object_name = "insurance_list"
    template_name = "insurances/search_results.html"
    login_url = "account_login"
    permission_required = "insurances.special_status"
    
    def get_queryset(self):
        query = self.request.GET.get("q")
        return Insurance.objects.filter(
            Q(customer=self.request.user) & (
                Q(line_of_business__icontains=query) | 
                Q(policy_number__icontains=query) |
                Q(insurer__icontains=query) |
                Q(policy_holder__icontains=query) |
                Q(premium__icontains=query)
            )
        )