from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django_recaptcha.fields import ReCaptchaField

from .models import Document



class CustomUserCreationForm(UserCreationForm):
    
    captcha = ReCaptchaField()
    
    class Meta:
        model = get_user_model()
        fields = (
            # "username", -> not needed - email=username
            "email",
            # password field is included by default
            # Personal Data
            "first_name",
            "last_name",
            "birth_date",
            "place_of_birth",
            "marital_status",
            "nationality",
            # Location Data
            "street",
            "house_number",
            "city",
            "postal_code",
            # Contact Data
            "phone_number",
            # Finance Data
            "iban",
            "bic",
            "financial_institution",
            # User Files
            "profile_picture"
        )


class CustomUserChangeForm(UserChangeForm):
    
    class Meta:
        model = get_user_model()
        fields = (
            # Need username as well to keep Value in Changes
            "username",
            "email",
            # password field is included by default
            # Personal Data
            "first_name",
            "last_name",
            "birth_date",
            "place_of_birth",
            "marital_status",
            "nationality",
            # Location Data
            "street",
            "house_number",
            "city",
            "postal_code",
            # Contact Data
            "phone_number",
            # Finance Data
            "iban",
            "bic",
            "financial_institution",
            # User Files
            "profile_picture",
        )

    ## Wait for "How-To" Web Security and 2FA        
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['password'].widget.attrs['readonly'] = True
        


class CustomAdminCreationForm(UserCreationForm):
    
    class Meta:
        model = get_user_model()
        fields = (
            "email",
            # "username",
            "name",
            "is_staff",        
        )
        
        

class CustomAdminChangeForm(UserChangeForm):
    
    class Meta:
        model = get_user_model()
        fields = (
            "email",
            # "username",
            "name",
            "is_staff",        
        )
        
        
        
class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['file']