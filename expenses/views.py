from django.shortcuts import redirect, render
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth import logout

from .forms import ExpenseSearchForm, SignUpForm
from .models import Expense, Category
from .reports import summary_per_category, summary_per_month, total_amount_spent, \
                    number_expenses_per_category


class ExpenseListView(LoginRequiredMixin, ListView):
    model = Expense
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        form = ExpenseSearchForm(self.request.GET)

        if form.is_valid():
            name = form.cleaned_data.get('name', '').strip()
            from_date = form.cleaned_data.get('from_date')
            to_date = form.cleaned_data.get('to_date')
            categories = form.cleaned_data.get('categories')

            if name:
                queryset = queryset.filter(name__icontains=name)
            if from_date:
                queryset = queryset.filter(date__gte=from_date)
            if to_date:
                queryset = queryset.filter(date__lte=to_date)
            if categories:
                queryset = queryset.filter(category__in=categories)

            sort_by = form.cleaned_data.get('sort_by')
            sort_order = form.cleaned_data.get('sort_order')

            if sort_by and sort_order:
                sort_by = f'-{sort_by}' if sort_order == 'desc' else sort_by
                queryset = queryset.order_by(sort_by)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ExpenseSearchForm(self.request.GET)
        context['summary_per_category'] = summary_per_category(self.object_list)
        context['total_amount_spent'] = total_amount_spent(self.object_list)
        context['summary_per_month'] = summary_per_month(self.object_list)
        return context


class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        counter_expenses = number_expenses_per_category()
        for category in context['object_list']:
            category.counter = counter_expenses.get(category.id, 0)

        return context


class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


def logout_view(request):
    logout(request)
    return redirect("home")
