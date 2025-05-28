from django.contrib import admin
from .models import Maxsulot, Comment, Categories

@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Maxsulot)
class MaxsulotAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'proce', 'last_price', 'views_count', 'published', 'categories', 'image', 'get_tags']
    list_filter = ['published', 'tags', 'categories']
    search_fields = ['title', 'body']
    prepopulated_fields = {'slug': ('title',)}

    def get_tags(self, obj):
        return ", ".join([tag.name for tag in obj.tags.all()])
    get_tags.short_description = 'Tags'

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = [ 'product', 'content', 'rating', 'created_at']
    list_filter = ['created_at',  'rating']
    search_fields = ['content']