from django.views.generic import UpdateView, DeleteView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, reverse_lazy
from .models import Expense, Category
from .views import ExpenseListView, CategoryListView, SignUpView, ExpensesCreateView, \
    CategoryCreateView

urlpatterns = [
    path('expense/list/',
         ExpenseListView.as_view(),
         name='expense-list'),
    path('expense/create/',
         ExpensesCreateView.as_view(),
         name='expense-create'),
    path('expense/<int:pk>/edit/',
         UpdateView.as_view(
             model=Expense,
             fields='__all__',
             success_url=reverse_lazy('expense-list'),
             template_name='generic_update.html'
         ),
         name='expense-edit'),
    path('expense/<int:pk>/delete/',
         DeleteView.as_view(
             model=Expense,
             success_url=reverse_lazy('expense-list'),
             template_name='generic_delete.html'
         ),
         name='expense-delete'),

    path('category/list/',
         CategoryListView.as_view(),
         name='category-list'),
    path('category/create/',
         CategoryCreateView.as_view(),
         name='category-create'),
    path('category/<int:pk>/edit/',
         UpdateView.as_view(
             model=Category,
             fields='__all__',
             success_url=reverse_lazy('category-list'),
             template_name='generic_update.html'
         ),
         name='category-edit'),
    path('category/<int:pk>/delete/',
         DeleteView.as_view(
             model=Category,
             success_url=reverse_lazy('category-list'),
             template_name='generic_delete.html'
         ),
         name='category-delete'),
    path('register/', SignUpView.as_view(), name='signup'),
    path('account/login/', LoginView.as_view(), name='login'),
    path('account/logout/', LogoutView.as_view(), name='logout'),
]
