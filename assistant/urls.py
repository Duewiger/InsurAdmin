from django.urls import path
from .views import InsuranceAssistantEmailView, InsuranceAssistantView

urlpatterns = [
    path('', InsuranceAssistantView.as_view(), name='assistant'),
    path('email_webhook/', InsuranceAssistantEmailView.as_view(), name='email_webhook'),
]