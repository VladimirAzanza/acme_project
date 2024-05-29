from django import forms

from .models import Birthday


class BirthdayForm(forms.ModelForm):
    '''
    first_name = forms.CharField(
        label='Имя', max_length=20
    )
    last_name = forms.CharField(
        label='Фамилия', required=False, help_text='Необязательное поле'
    )
    birthday = forms.DateField(
        label='Дата рождения',
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    '''
    class Meta:
        model = Birthday
        fields = '__all__'
        widgets = {
            'birthday': forms.DateInput(attrs={'type': 'date'})
        }
