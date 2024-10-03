from django.urls import path

from .views import InsuranceCreationView, InsuranceDeleteView, InsuranceEditView, InsuranceListView, InsuranceDetailView, SearchResultsView

urlpatterns = [
    path("", InsuranceListView.as_view(), name="insurance_list"),
    path("<uuid:pk>/", InsuranceDetailView.as_view(), name="insurance_detail"),
    path("<uuid:pk>/edit/", InsuranceEditView.as_view(), name="insurance_edit"),
    path("<uuid:pk>/delete/", InsuranceDeleteView.as_view(), name="insurance_delete"),
    path("search/", SearchResultsView.as_view(), name="search_results"),
    path("create-insurance/", InsuranceCreationView.as_view(), name="insurance_creation"),
]