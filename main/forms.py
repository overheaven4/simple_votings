from django import forms

class First_pageForm(forms.Form):
    first_num = forms.IntegerField(label="Первое число")
    second_num = forms.IntegerField(label="Второе число")