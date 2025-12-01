from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'password', 'username')

class PharmacistForm(forms.ModelForm):
    class Meta:
        model = Pharmacist
        fields = ('mobile', 'gender')

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ('companyname',)

class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = ('companyname', 'medicinename', 'batchnumber', 'mgfdate', 'expirydate', 'quantity', 'price',)


