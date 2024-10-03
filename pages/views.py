from typing import Any
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView

from insurances.models import Insurance


class HomePageView(TemplateView):
    template_name = "home.html"
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('account_login')
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        insurance_list = Insurance.objects.filter(customer=self.request.user)[:3]
        context['insurance_list'] = insurance_list
        return context