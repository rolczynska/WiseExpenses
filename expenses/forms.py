from django import forms
from .models import Expense, Category


class ExpenseSearchForm(forms.ModelForm):

    from_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    to_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    sort_by = forms.ChoiceField(
        choices=[('date', 'Date'), ('category', 'Category')],
        required=False,
        initial='date'
    )
    sort_order = forms.ChoiceField(
        choices=[('asc', 'Ascending'), ('desc', 'Descending')],
        required=False,
        initial='asc'
    )

    class Meta:
        model = Expense
        fields = ('name',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = False
