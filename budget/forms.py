from inspect import Attribute
from tkinter import Widget
from django.forms import ModelForm
from django import forms
from .models import Budget,Actuals,Category





class budget_form(ModelForm):

    def __init__(self,*args, user=None, **kwargs):
        super(budget_form, self).__init__(*args, **kwargs)
        if user is not None:
            self.fields['category'].queryset = Category.objects.filter(user=user)




    class Meta:
        model = Budget
        fields = ['category','date','budget_amt','comments' ]
        widgets = {
            
            'category' : forms.Select(attrs={'class':'form-control'}),
            'date' : forms.DateInput(attrs={'class':'form-control'}),
            'budget_amt' : forms.NumberInput(attrs={'class':'form-control'}),
            'comments' : forms.TextInput(attrs={'class':'form-control'}),
        }

class actuals_form(ModelForm):

    def __init__(self,*args, user=None, **kwargs):
        super(actuals_form, self).__init__(*args, **kwargs)
        if user is not None:
            self.fields['category'].queryset = Category.objects.filter(user=user)



    class Meta:
        model = Actuals
        fields = '__all__'

        widgets = {
            
            'category' : forms.Select(attrs={'class':'form-control'}),
            'date' : forms.DateInput(attrs={'class':'form-control'}),
            'transactions_amount' : forms.NumberInput(attrs={'class':'form-control'}),
            'vendor' : forms.TextInput(attrs={'class':'form-control'}),
            'details': forms.TextInput(attrs={'class':'form-control'}),
            
        }

class categories_form(ModelForm):
    
    
    class Meta:
        model = Category
        fields = '__all__'
        widgets = {'user': forms.HiddenInput()}


class date_form(forms.Form): 
    INTEGER_CHOICES = [('01','January'),('02', 'February'),('03','March'),('04','April'),('05','May'),('06','June'),('07','July'),('08','August'),('09','September'),('10','October'),('11','November'),('12','December')]
    YEAR_CHOICE = [('2019',2019),('2020', 2020),('2021',2021),('2022',2022),('2023',2023),('2024',2024)]

    months = forms.CharField(label='Month',required=False,widget=forms.Select(choices=INTEGER_CHOICES,attrs={'class':'form-control-sm'}))

    years = forms.CharField(label='Year',required=False,widget=forms.Select(choices=YEAR_CHOICE,attrs={'class':'form-control-sm'}))

 

class year_form(forms.Form):
    YEAR_CHOICE = [('2019',2019),('2020', 2020),('2021',2021),('2022',2022),('2023',2023),('2024',2024)]
    years = forms.CharField(label='Year',required=False,widget=forms.Select(choices=YEAR_CHOICE,attrs={'class':'form-control'}))
