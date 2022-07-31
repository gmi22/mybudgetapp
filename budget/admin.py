from django.contrib import admin
from .models import Budget,Actuals,Category

# Register your models here.


admin.site.register(Budget)
admin.site.register(Actuals)
admin.site.register(Category)
