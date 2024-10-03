from django import forms
from .models import Insurance



class InsuranceForm(forms.ModelForm):
    class Meta:
        model = Insurance
        fields = '__all__'   
       
           
        
class InsuranceChangeForm(forms.ModelForm):
    class Meta:
        model = Insurance
        fields = '__all__'