from django.contrib import admin
from . import models


@admin.register(models.AuthUser)
class AuthUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'nickname', 'email', 'join_date')
    list_display_links = ('email',)


@admin.register(models.SocialLink)
class AuthUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'link')
