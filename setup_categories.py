#!/bin/bash

# Script to set up default expense categories
# Run with: python manage.py shell < setup_categories.py

from expenses.models import Category

categories = [
    {'name': 'Food & Dining', 'icon': 'utensils',
        'color': '#f59e0b', 'is_default': True},
    {'name': 'Transport', 'icon': 'car', 'color': '#3b82f6', 'is_default': True},
    {'name': 'Shopping', 'icon': 'shopping-bag',
        'color': '#ec4899', 'is_default': True},
    {'name': 'Entertainment', 'icon': 'film',
        'color': '#8b5cf6', 'is_default': True},
    {'name': 'Bills & Utilities', 'icon': 'file-text',
        'color': '#ef4444', 'is_default': True},
    {'name': 'Healthcare', 'icon': 'heart', 'color': '#10b981', 'is_default': True},
    {'name': 'Education', 'icon': 'book', 'color': '#06b6d4', 'is_default': True},
    {'name': 'Personal Care', 'icon': 'user',
        'color': '#f43f5e', 'is_default': True},
    {'name': 'Travel', 'icon': 'plane', 'color': '#6366f1', 'is_default': True},
    {'name': 'Other', 'icon': 'tag', 'color': '#64748b', 'is_default': True},
]

for cat_data in categories:
    category, created = Category.objects.get_or_create(
        name=cat_data['name'],
        defaults=cat_data
    )
    if created:
        print(f"Created category: {category.name}")
    else:
        print(f"Category already exists: {category.name}")

print("\nDefault categories setup complete!")
