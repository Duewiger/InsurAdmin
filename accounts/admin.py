from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from insurances.models import Insurance
from .forms import CustomAdminCreationForm, CustomAdminChangeForm
from .models import Document, Registration

CustomUser = get_user_model()

# Inline Admin for Insurances
class InsuranceInline(admin.TabularInline):
    model = Insurance

class CustomAdminUser(UserAdmin):
    inlines = (InsuranceInline,)
    add_form = CustomAdminCreationForm
    form = CustomAdminChangeForm
    model = CustomUser
    list_display = [
        "email",
        # "username",
        "name",
        "is_staff",
    ]
    fieldsets = UserAdmin.fieldsets + (
        # Für Admins
        (None, {'fields': ('name',)}),
        # Für Kunden
        ('Customer Info', {'fields': ('salutation', 'birth_date', 'place_of_birth', 'marital_status', 'nationality', 'street', 'house_number', 'city', 'postal_code', 'phone_number', 'iban', 'bic', 'financial_institution', 'profile_picture')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        # Für Admins
        (None, {'fields': ('name',)}),
        # Für Kunden
        ('Customer Info', {'fields': ('salutation', 'birth_date', 'place_of_birth', 'marital_status', 'nationality', 'street', 'house_number', 'city', 'postal_code', 'phone_number', 'iban', 'bic', 'financial_institution', 'profile_picture')}),
    )

admin.site.register(CustomUser, CustomAdminUser)
admin.site.register(Document)
admin.site.register(Registration)