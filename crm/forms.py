from django import forms
from django.forms import ModelForm
from jalali_date.fields import JalaliDateField, SplitJalaliDateTimeField
from jalali_date.widgets import AdminJalaliDateWidget, AdminSplitJalaliDateTime
from .models import Order_incomings, Customer, Product
from . import models




#------------------------------------------------------------------------------
class TimeForm(forms.ModelForm):
    class Meta:
        model = Order_incomings
        fields = ('date_created',)

    def __init__(self, *args, **kwargs):
        super(TimeForm, self).__init__(*args, **kwargs)
        self.fields['date_created'] = JalaliDateField( widget=AdminJalaliDateWidget(attrs={'style':'width:15px; height:37px'}) )
        self.fields['date_created'].required = True
        self.fields['date_created'].label = False




'''
#------------------------------------------------------------------------------
class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('product_tag',)

    def __init__(self, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)
        self.fields['product_tag'] = forms.ModelMultipleChoiceField(queryset=Product.objects.all(), widget=forms.CheckboxSelectMultiple )
        self.fields['product_tag'].required = False
        self.fields['product_tag'].label = False
'''








#
