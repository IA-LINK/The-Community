from django.contrib import admin
from .models import Category, Post, Comment

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'updated_at')
    list_filter = ('created_at', 'author', 'categories')
    search_fields = ('title', 'content')
    ordering = ('-created_at',)
    

class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'created_at')
    search_fields = ('author__username', 'content')
    list_filter = ('created_at', 'author')

# Register your models with the admin site
admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
