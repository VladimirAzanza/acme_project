from django.shortcuts import render

from .forms import BirthdayForm


def birthday(request):
    return render(
        request,
        'birthday/birthday.html',
        context={
            'form': BirthdayForm()
        }
    )
