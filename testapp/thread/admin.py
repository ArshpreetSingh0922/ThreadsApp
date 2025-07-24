from django.contrib import admin
from .models import ThreadPost, Comment

@admin.register(ThreadPost)
class ThreadPostAdmin(admin.ModelAdmin):
    list_display = ('postid', 'owner', 'content')
    search_fields = ('owner__username', 'content')
    

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('commentid', 'post', 'owner', 'commenttext')
    search_fields = ('owner__username', 'commenttext')

