from django import forms

class InputForm(forms.Form):
    input = forms.CharField(max_length=1000, required=True,
                            widget = forms.TextInput(attrs={
                                "placeholder": "Place your message here...",
                                "class": "user-input"
                            }))
    
    class Meta:
        fields = ('input',)