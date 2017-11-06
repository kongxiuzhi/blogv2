from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User 
# Register your models here.

class ProfileInline(admin.StackedInline):
    model = Profile 
    can_delete = False
    verbose_name_plural = 'profile'

class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)

admin.site.unregister(User)
admin.site.register(User,UserAdmin)


def make_published(modeladmin,request,queryset):
    queryset.update(publish=True)
make_published.short_description = "一键发表"
def make_unpublished(modeladmin,request,queryset):
    queryset.update(publish=False)
make_unpublished.short_description = "一键取消发表"

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display=("title","author","publish","created","updated","draft")
    list_editable = ("publish",)
    list_filter = ("created","updated","publish","draft")
    raw_id_fields = ("author",)
    search_fields = ["title","author","created"]
    date_hierarchy="created"
    actions = [make_unpublished,make_published]


def make_comments_unpublished(modeladmin,request,queryset):
    queryset.update(active=False)
make_comments_unpublished.short_description = "一键取消发表"

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display=('author',"active")
    list_editable = ("active",)
    list_filter = ("created","updated","active")
    search_fields = ["article","author","created"]
    date_hierarchy="created"
    actions=[make_comments_unpublished,]
