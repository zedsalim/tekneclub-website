from django.contrib import admin
from .models import *

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'post_type', 'created_at', 'updated_at')
    search_fields = ('title', 'content', 'author__username') 
    list_filter = ('status', 'post_type', 'categories', 'created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('title', 'content', 'slug', 'status', 'post_type', 'author', 'categories')
        }),
        ('Date Information', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    list_editable = ('status', 'post_type')


admin.site.register(Post, PostAdmin)
admin.site.register(PostImages)
admin.site.register(Category)
