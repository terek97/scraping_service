from django import forms

from .models import City, Profession


class FindForm(forms.Form):
    city = forms.ModelChoiceField(
        queryset=City.objects.all(), empty_label="",
        to_field_name='slug', required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Город',
    )

    profession = forms.ModelChoiceField(
        queryset=Profession.objects.all(), empty_label="",
        to_field_name='slug', required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Ключевой навык',
    )
