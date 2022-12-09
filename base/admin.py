from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Post, PostImage, Tag, Comment, Reply


# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'get_photo', 'get_likes')
    search_fields = ('caption', 'user')
    list_filter = ('user',)
    fields = ('user', 'caption', 'main_image', 'created_at', 'likes')
    readonly_fields = ('created_at',)

    def get_likes(self, obj):
        return len(obj.likes.all())

    def get_photo(self, obj):
        if obj.main_image:
            return mark_safe(f'<img src={obj.main_image.url} width=75>')
        else:
            return 'Post has not photo'

    get_photo.short_description = 'Photo'
    get_likes.short_description = 'likes'


class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'caption', 'get_posts')


class PostImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'get_image')

    def get_image(self, obj):
        if obj.image:
            return mark_safe(f'<img src={obj.image.url} width=75>')
        else:
            return 'Post has not image'

    get_image.short_description = 'Image'


class LikePostAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'post')
    list_filter = ('user', 'post')


admin.site.register(Post, PostAdmin)
admin.site.register(PostImage, PostImageAdmin)
# admin.site.register(LikePost, LikePostAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Comment)
admin.site.register(Reply)
