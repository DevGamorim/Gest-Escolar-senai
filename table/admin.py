from django.contrib import admin
from django.contrib.auth import admin as auth_admin

from .forms import UserChangeForm, UserCreationForm
from .models import user
# Register your models here.

@admin.register(user)
class UserAdmin(auth_admin.UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    model = user
    fieldsets = auth_admin.UserAdmin.fieldsets + (
        ("Privilégio", {"fields": ("privilegio",)}),
    )
