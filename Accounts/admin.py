from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserProfileModel, UserPost, PostComment
from django.contrib.auth.models import User


class ProfileAdmin(admin.StackedInline):
    model = UserProfileModel
    can_delete = False


class ProfileExtended(UserAdmin):
    inlines = (ProfileAdmin,)


admin.site.unregister(User)
admin.site.register(User, ProfileExtended)


@admin.register(UserPost)
class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'body', 'created', 'updated')


@admin.register(PostComment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('body',)
