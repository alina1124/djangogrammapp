from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Profile

# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'bio', 'get_avatar')

    def get_avatar(self, obj):
        return mark_safe(f'<img src={obj.avatar.url} width=75>')

    get_avatar.short_description = 'Avatar'


# class FollowerAdmin(admin.ModelAdmin):
#     list_display = ('id', 'user', 'follower')


admin.site.register(Profile, ProfileAdmin)
# admin.site.register(Follower, FollowerAdmin)