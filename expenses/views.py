from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

from .forms import ExpenseSearchForm, SignUpForm
from .models import Expense, Category
from .reports import summary_per_category, summary_per_month, total_amount_spent, \
                    number_expenses_per_category


class ExpenseListView(LoginRequiredMixin, ListView):
    model = Expense
    paginate_by = 5

    def get_queryset(self):
        # Filter expenses to those belonging to the logged-in user and apply search criteria.
        queryset = Expense.objects.filter(user=self.request.user)
        form = ExpenseSearchForm(self.request.GET, user=self.request.user)

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
        context['form'] = ExpenseSearchForm(self.request.GET, user=self.request.user)
        context['summary_per_category'] = summary_per_category(self.object_list)
        context['total_amount_spent'] = total_amount_spent(self.object_list)
        context['summary_per_month'] = summary_per_month(self.object_list)
        return context


class ExpensesCreateView(CreateView):
    model = Expense
    fields = ['name', 'amount', 'category', 'date']
    success_url = reverse_lazy('expense-list')
    template_name = "generic_update.html"

    def form_valid(self, form):
        # Link the expense to the logged-in user.
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_form(self, form_class=None):
        # Limit category choices to those created by the logged-in user.
        form = super(ExpensesCreateView, self).get_form(form_class)
        form.fields['category'].queryset = Category.objects.filter(user=self.request.user)
        return form


class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    paginate_by = 5

    def get_queryset(self):
        # Filter categories to those belonging to the logged-in user.
        return Category.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        counter_expenses = number_expenses_per_category()
        for category in context['object_list']:
            category.counter = counter_expenses.get(category.id, 0)

        return context


class CategoryCreateView(CreateView):
    model = Category
    fields = ['name']
    success_url = reverse_lazy('category-list')
    template_name = "generic_update.html"

    def form_valid(self, form):
        # Link the category to the logged-in user.
        form.instance.user = self.request.user
        return super().form_valid(form)


class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"
