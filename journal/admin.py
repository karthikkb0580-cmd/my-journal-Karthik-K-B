from django.contrib import admin

from .models import Article, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "is_published", "created_at")
    list_filter = ("is_published", "categories", "created_at")
    search_fields = ("title", "subtitle", "body", "author__username")
    filter_horizontal = ("categories",)
    readonly_fields = ("created_at", "updated_at")
