from django import forms
from .models import uploadpdf

# created forms for handlingforms
class dataform(forms.ModelForm):
    class Meta:
        model=uploadpdf
        fields= ('pdf',)