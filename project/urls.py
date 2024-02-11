from django.urls import include, path
from django.views.generic.base import RedirectView
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('expenses.urls')),
    path('',
         RedirectView.as_view(pattern_name='expense-list'),
         name='home'),
]
