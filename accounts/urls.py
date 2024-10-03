from django.urls import path
from .views import AccountPageView, AccountDataEditView, AccountDeleteView, SignupPageView, DocumentUploadView, AccountLockedView, CustomLoginView, VerifyCodeView

urlpatterns = [
    path("", AccountPageView.as_view(), name="account_data_list"),
    path("signup/", SignupPageView.as_view(), name="signup"),
    path("account-login/", CustomLoginView.as_view(), name="account_login"),
    path("verify/", VerifyCodeView.as_view(), name="verify_code"),
    path("<uuid:pk>/", AccountDataEditView.as_view(), name="account_data_edit"),
    path("<uuid:pk>/delete/", AccountDeleteView.as_view(), name="account_delete"),
    path('upload-document/', DocumentUploadView.as_view(), name='upload_document'),
    path("account_locked/", AccountLockedView.as_view(), name="account_locked"),
]