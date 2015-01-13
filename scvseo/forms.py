from django import forms


class MainForm(forms.Form):
    result_ranks = forms.FileField(label='File with Result Rankings')
    website_list = forms.FileField(label='List of Websites')