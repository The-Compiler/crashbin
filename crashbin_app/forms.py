from django import forms
from .models import Bin


class BinForm(forms.ModelForm):

    class Meta:
        model = Bin
        fields = 'name', 'description', 'maintainers', 'labels'


class ReportReplyForm(forms.Form):

    typ = forms.ChoiceField(choices=[
        ('Reply', 'Reply'),
        ('Note', 'Note'),
    ])
    text = forms.CharField()
