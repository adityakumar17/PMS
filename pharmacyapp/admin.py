from django.contrib import admin
from pharmacyapp.models import *

# Register your models here.
admin.site.register(Pharmacist)
admin.site.register(Company)
admin.site.register(Medicine)
admin.site.register(Order)
admin.site.register(Cart)
admin.site.register(History)