from django import forms
from .models import Recipe, Ingredient
from django.forms import modelformset_factory

class IngredientCreateForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = [
            'id',
            'name',
            'rcp_sub_num',
            'rcp_sub_nm',
            'rcp_ingrdnt_nm',
            'rcp_ingrdnt_qnt',
            'rcp_ingrdnt_unit',
            'rcp_ingrdnt_sub',
        ]
        
        widgets = {
            'rcp_num': forms.HiddenInput(),
            'rcp_nm': forms.HiddenInput(),
        }
        

class RcpFormsetForm(forms.ModelForm):
    error_css_class = "required"
    class Meta:
        model = RcpTable
        fields = [
            'rcp_pk',
            'rcp_num',
            'rcp_nm',
            'rcp_sub_num',
            'rcp_sub_nm',
            'rcp_ingrdnt_nm',
            'rcp_ingrdnt_qnt',
            'rcp_ingrdnt_unit',
            'rcp_ingrdnt_sub',
        ]
        
        widgets = {
            'rcp_pk': forms.HiddenInput(),
            'rcp_num': forms.HiddenInput(),
            'rcp_nm': forms.HiddenInput(),
        }
        
        
RcpFormSet = modelformset_factory(RcpTable, form=RcpFormsetForm)


"""RcpCreateFormSet = modelformset_factory(RcpTable,fields=(
    'rcp_sub_num',
    'rcp_sub_nm',
    'rcp_ingrdnt_nm',
    'rcp_ingrdnt_qnt',
    'rcp_ingrdnt_unit',
    'rcp_ingrdnt_sub'
    ), extra=1)

class RcpNmCreateForm(forms.ModelForm):
    class Meta:
        model = RcpTable
        fields = ['rcp_nm']"""
