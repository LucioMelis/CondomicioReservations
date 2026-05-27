from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from apps.user.models import User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):

    list_display = DjangoUserAdmin.list_display + ("phone_number", "address", "city", "zip_code", "country", "deleted")
    fieldsets = DjangoUserAdmin.fieldsets + (
        ("Address",
         {"fields": ["phone_number", "address", "city", "zip_code", "country"]}),) + (
                    ("Status", {"fields": ["deleted"]}),)

    add_fieldsets = DjangoUserAdmin.add_fieldsets + (
        (("Contact & Address"), {
            "classes": ("wide",),
            "fields": ["phone_number", "address", "city", "zip_code", "country"],
        }),
        (("Status"), {
            "classes": ("wide",),
            "fields": ["deleted"],
        }),
    )
