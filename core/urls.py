from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Djoser auth endpoints
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    # App endpoints
    path('users/',     include('users.urls')),
    path('expenses/',  include('expenses.urls')),
    path('budgets/',   include('budgets.urls')),
    path('savings/', include('savings.urls')),
    path('analytics/', include('analytics.urls')),
    path('reports/', include('reports.urls')),
]
