from django import forms
from cards.models import Product, Filling, Area, Confectioner
from django.conf import settings
from django.contrib.auth.models import User


class SearchForm(forms.Form):
    product = forms.ModelChoiceField(queryset=Product.objects.all(),
                                     required=False,
                                     widget=forms.RadioSelect,
                                     blank=True,
                                     label='Тип')
    fillings = forms.ModelMultipleChoiceField(queryset=Filling.objects.all(),
                                              widget=forms.CheckboxSelectMultiple,
                                              required=False,
                                              label='Начинки')
    min_price = forms.IntegerField(min_value=0,
                                   required=False,
                                   widget=forms.HiddenInput,
                                   max_value=10000)
    max_price = forms.IntegerField(min_value=0,
                                   required=False,
                                   widget=forms.HiddenInput,
                                   max_value=10000)
    area = forms.ModelChoiceField(queryset=Area.objects.all(),
                                  required=False,
                                  label='Район')


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ConfectionerForm(forms.ModelForm):
    class Meta:
        model = Confectioner
        fields = ('fullName', 'area', 'telegram')
