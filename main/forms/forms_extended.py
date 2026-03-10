from django import forms
from django.contrib.auth.models import User
from main.models import Voting


class VotingSearchForm(forms.Form):
    """
    Форма для расширенного поиска и фильтрации голосований.
    """
    search_query = forms.CharField(
        max_length=100,
        required=False,
        label='Поиск по названию',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите текст...'})
    )

    date_from = forms.DateField(
        required=False,
        label='Дата от',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )

    date_to = forms.DateField(
        required=False,
        label='Дата до',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )

    sort_by = forms.ChoiceField(
        choices=[
            ('-created_at', 'Сначала новые'),
            ('created_at', 'Сначала старые'),
            ('title', 'По алфавиту (А-Я)'),
            ('-title', 'По алфавиту (Я-А)'),
        ],
        required=False,
        label='Сортировка',
        widget=forms.Select(attrs={'class': 'form-select'})
    )


class UserProfileUpdateForm(forms.ModelForm):
    """
    Форма для редактирования профиля пользователя (имя, email).
    """

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'email': 'Электронная почта'
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }