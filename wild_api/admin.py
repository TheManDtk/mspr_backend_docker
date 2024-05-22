from django.contrib import admin

# Register your models here.
from .models import InfoEspeces, Soumission

admin.site.register(InfoEspeces)
admin.site.register(Soumission)