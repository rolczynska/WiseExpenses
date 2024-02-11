from django import forms
from .models import Expense, Category
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


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
        choices=[('desc', 'Descending'), ('asc', 'Ascending')],
        required=False,
        initial='desc'
    )

    class Meta:
        model = Expense
        fields = ('name',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = False


class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'Username',
                                                             'class': 'form-control',
                                                             }))
    password1 = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Password',
                                                                  'class': 'form-control',
                                                                  'data-toggle': 'password',
                                                                  'id': 'password',
                                                                  }))
    password2 = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password',
                                                                  'class': 'form-control',
                                                                  'data-toggle': 'password',
                                                                  'id': 'password',
                                                                  }))

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
