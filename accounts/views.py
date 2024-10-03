from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect
from django.views.generic.edit import FormView

from django.conf import settings
from twilio.rest import Client
from django.contrib.auth import authenticate, login, get_backends

from .forms import CustomUserCreationForm, CustomUserChangeForm, DocumentForm
from .models import CustomUser, Document



class SignupPageView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("account-login")
    template_name = "registration/signup.html"
    
    
    
class AccountPageView(LoginRequiredMixin, ListView):
    model = CustomUser
    context_object_name = "account_data_list"
    template_name = "accounts/account_data_list.html"
    login_url = "account_login"
    
    def get_queryset(self):
        return CustomUser.objects.filter(id=self.request.user.id)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['documents'] = Document.objects.filter(user=self.request.user)
        return context



class AccountDataEditView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = "accounts/account_data_edit.html"
    login_url = "account_login"
    success_url = reverse_lazy("account_data_list")
    
    def form_valid(self, form):
        profile_picture = self.request.FILES.get('profile_picture')
        if profile_picture:
            form.instance.profile_picture = profile_picture
        return super().form_valid(form)
    
    
class AccountDeleteView(LoginRequiredMixin, DeleteView):
    model = CustomUser
    template_name = "accounts/account_delete.html"
    login_url = "account_login"
    success_url = reverse_lazy("account_login")
    
    def get_object(self, queryset=None):
        return CustomUser.objects.get(id=self.request.user.id)



class DocumentUploadView(FormView):
    template_name = 'accounts/document_upload.html'
    form_class = DocumentForm

    def form_valid(self, form):
        document = form.save(commit=False)
        document.user = self.request.user
        document.save()
        return redirect('account_data_list')
    
    

class AccountLockedView(View):
    template_name = 'accounts/account_locked.html'
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
    

class CustomLoginView(View):
    template_name = 'accounts/account_login.html'

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        context = {'error': ''}  # Initialize context with empty error message
        if user is not None:
            # Send verification code via Twilio
            if not user.phone_number:
                context['error'] = 'Phone number not provided'
                return render(request, self.template_name, context)

            account_sid = settings.TWILIO_ACCOUNT_SID
            auth_token = settings.TWILIO_AUTH_TOKEN
            service_sid = settings.TWILIO_VERIFICATION_SERVICE_SID

            client = Client(account_sid, auth_token)

            # Ensure phone number is in E.164 format
            phone_number = user.phone_number
            if not phone_number.startswith('+'):
                phone_number = '+49' + phone_number.lstrip('0')

            client.verify \
                .v2 \
                .services(service_sid) \
                .verifications \
                .create(to=phone_number, channel='sms')

            request.session['user_id'] = str(user.id)
            # Set the backend path explicitly
            request.session['backend'] = 'django.contrib.auth.backends.ModelBackend'
            return redirect('verify_code')
        else:
            context['error'] = 'Invalid credentials'
            return render(request, self.template_name, context)

    def get(self, request, *args, **kwargs):
        context = {'error': ''}
        return render(request, self.template_name, context)


class VerifyCodeView(View):
    template_name = 'accounts/verify_code.html'

    def post(self, request, *args, **kwargs):
        code = request.POST.get('code')
        user_id = request.session.get('user_id')
        backend_path = request.session.get('backend')
        context = {'error': ''}  # Initialize context with empty error message
        if user_id and backend_path:
            user = CustomUser.objects.get(id=user_id)
            account_sid = settings.TWILIO_ACCOUNT_SID
            auth_token = settings.TWILIO_AUTH_TOKEN
            service_sid = settings.TWILIO_VERIFICATION_SERVICE_SID

            client = Client(account_sid, auth_token)

            # Ensure phone number is in E.164 format
            phone_number = user.phone_number
            if not phone_number.startswith('+'):
                phone_number = '+49' + phone_number.lstrip('0')

            verification_check = client.verify \
                .v2 \
                .services(service_sid) \
                .verification_checks \
                .create(to=phone_number, code=code)

            if verification_check.status == "approved":
                # Explicitly set the backend
                user.backend = backend_path
                login(request, user)
                del request.session['user_id']
                del request.session['backend']
                return redirect('account_data_list')
            else:
                context['error'] = 'Invalid code'
                return render(request, self.template_name, context)
        else:
            return redirect('account_login')

    def get(self, request, *args, **kwargs):
        context = {'error': ''}
        return render(request, self.template_name, context)