from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

UserAdmin.list_filter += ('username', 'email',)

