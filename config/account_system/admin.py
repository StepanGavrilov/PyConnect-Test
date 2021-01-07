from django.contrib import admin

from .models import Account


@admin.register(Account)
class AdminAccount(admin.ModelAdmin):
    list_display = ('id', 'username', 'last_login')
