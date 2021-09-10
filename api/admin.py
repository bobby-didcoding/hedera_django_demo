from django.contrib import admin
from . models import Invoicing


# DOCS - https://docs.djangoproject.com/en/3.1/ref/contrib/admin/

class InvoicingAdmin(admin.ModelAdmin):
	
	list_display = ('id', 'user', 'timestamp')

admin.site.register(Invoicing,InvoicingAdmin)