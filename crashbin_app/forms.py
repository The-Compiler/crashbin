from django import forms
from .models import Bin


class BinForm(forms.ModelForm):

    class Meta:
        model = Bin
        fields = 'name', 'description', 'maintainers', 'labels'
