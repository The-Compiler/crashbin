from django import forms
from .models import Bin, Label


class BinForm(forms.ModelForm):

    class Meta:
        model = Bin
        fields = 'name', 'description'


class LabelForm(forms.ModelForm):

    class Meta:
        model = Label
        fields = 'name', 'color', 'description'


class ReportReplyForm(forms.Form):

    typ = forms.ChoiceField(choices=[
        ('Reply', 'Reply'),
        ('Note', 'Note'),
    ])
    text = forms.CharField()
