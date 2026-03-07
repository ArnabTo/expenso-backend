from django.contrib import admin
from .models import Category, Expense

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon', 'color', 'is_default', 'created_by')
    list_filter = ('is_default',)

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'amount', 'category', 'date')
    list_filter = ('category', 'date')
    search_fields = ('title', 'user__email')
    ordering = ('-date',)
