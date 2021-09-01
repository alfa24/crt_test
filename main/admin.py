from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from main.models import UserProfile, City, Advert

User = get_user_model()


class ProfileInlineAdmin(admin.StackedInline):
    """Профиль администратора."""
    extra = 1
    model = UserProfile
    fields = ['city']


class MainUserAdmin(UserAdmin):
    """Переопределенный раздел пользователя с отображением профиля"""
    inlines = [ProfileInlineAdmin]


admin.site.register(City)
admin.site.register(Advert)
admin.site.unregister(User)
admin.site.register(User, MainUserAdmin)
