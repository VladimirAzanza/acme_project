from django import forms
from django.core.exceptions import ValidationError

from .models import Birthday, Congratulation


class BirthdayForm(forms.ModelForm):
    '''
        forms.Form are used if there is no associated model:

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
        exclude = ('author',)
        widgets = {
            'birthday': forms.DateInput(attrs={'type': 'date'})
        }

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        return first_name.split()[0]

    def clean(self):
        super().clean()
        '''
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        if Birthday.objects.filter(
            first_name=first_name,
            last_name=last_name
        ):
            raise ValidationError(
                'введите, пожалуйста, другое имя'
            )
        '''


class CongratulationForm(forms.ModelForm):

    class Meta:
        model = Congratulation
        fields = ('text',)
