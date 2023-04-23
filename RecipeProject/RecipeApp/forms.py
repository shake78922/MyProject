from django import forms
from .models import RcpTable
from django.forms import formset_factory, modelformset_factory

class IngrdntCreateForm(forms.ModelForm):
    class Meta:
        model = RcpTable
        fields = [
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
            'rcp_num': forms.HiddenInput(),
            'rcp_nm': forms.HiddenInput(),
        }

class RcpCreateForm(forms.ModelForm):
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
        }



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
