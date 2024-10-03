"""
URL configuration for insuradmin_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

# from two_factor.urls import urlpatterns as tf_urls
# from two_factor.gateways.twilio.urls import urlpatterns as tf_twilio_urls


urlpatterns = [
    # Django admin
    path("insuradmin-admins/", admin.site.urls),
    # External apps
    # # User management
    path("accounts/", include("allauth.urls")),
    # # 2FA
    # path("", include(tf_urls)),
    # path('', include(tf_twilio_urls)),
    # Local apps
    path("", include("pages.urls")),
    path("accounts/", include("accounts.urls")),
    path("insurances/", include("insurances.urls")),
    path("processes/", include("processes.urls")),
    path("assistant/", include("assistant.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)