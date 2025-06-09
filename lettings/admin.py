# lettings/admin.py
from django.contrib import admin

from .models import Address, Letting


class AddressAdmin(admin.ModelAdmin):
    list_display = ("number", "street", "city", "state", "zip_code", "country_iso_code")
    search_fields = ("street", "city")


class LettingAdmin(admin.ModelAdmin):
    list_display = ("title", "address")
    search_fields = ("title",)


# Enregistrement sans décorateur
admin.site.register(Address, AddressAdmin)
admin.site.register(Letting, LettingAdmin)
