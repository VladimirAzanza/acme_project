# from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import (
    LoginRequiredMixin, UserPassesTestMixin
)
from django.contrib.auth.decorators import login_required
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)
from django.urls import reverse_lazy

from .forms import BirthdayForm, CongratulationForm
from .models import Birthday, Congratulation
from .utils import calculate_birthday_countdown


@login_required
def add_comment(request, pk):
    birthday = get_object_or_404(Birthday, pk=pk)
    form = CongratulationForm(request.POST)
    if form.is_valid():
        congratulation = form.save(commit=False)
        congratulation.author = request.user
        congratulation.birthday = birthday
        congratulation.save()
    return redirect('birthday:detail', pk=pk)


class BirthdayFormMixin:
    form_class = BirthdayForm
    # if template name is birthday_form we dont have to write template_name.
    template_name = 'birthday/birthday.html'


class OnlyAuthorMixin(UserPassesTestMixin):

    def test_func(self):
        object = self.get_object()
        return object.author == self.request.user


class BirthdayCreateView(
    BirthdayFormMixin, LoginRequiredMixin, CreateView
):
    model = Birthday

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class BirthdayUpdateView(
    BirthdayFormMixin, LoginRequiredMixin, OnlyAuthorMixin, UpdateView
):
    model = Birthday


class BirthdayDetailView(
    LoginRequiredMixin, DetailView
):
    model = Birthday

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['birthday_countdown'] = calculate_birthday_countdown(
            self.object.birthday
        )
        context['form'] = CongratulationForm()
        context['congratulations'] = (
            self.object.congratulations.select_related('author')
        )
        return context


class BirthdayListView(
    LoginRequiredMixin, ListView
):
    model = Birthday
    queryset = Birthday.objects.prefetch_related(
        'tags'
    ).select_related(
        'author'
    )
    ordering = 'id'
    paginate_by = 10


class BirthdayDeleteView(
    LoginRequiredMixin, OnlyAuthorMixin, DeleteView
):
    model = Birthday
    success_url = reverse_lazy('birthday:list')


'''
    Below the same code as BirthdayCreate(Update)View but written as
    a view function:
    def birthday(request, pk=None):
        if pk is not None:
            instance = get_object_or_404(
                Birthday,
                pk=pk
            )
        else:
            instance = None
        form = BirthdayForm(
            request.POST or None,
            files=request.FILES or None,
            instance=instance
        )
        context = {'form': form}
        if form.is_valid():
            form.save()
            birthday_countdown = calculate_birthday_countdown(
                form.cleaned_data['birthday']
            )
            context.update(
                {
                    'birthday_countdown': birthday_countdown
                }
            )
        return render(
            request,
            'birthday/birthday.html',
            context
        )
'''

'''
    Below the same code as BirthdayListView but written as a view function:
    def birthday_list(request):
        birthdays = Birthday.objects.order_by('id')
        paginator = Paginator(birthdays, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            'page_obj': page_obj
        }
        return render(
            request,
            'birthday/birthday_list.html',
            context
        )
'''

'''
    Below the same code as BirthdayListView but written as a view function:
    def delete_birthday(request, pk):
        instance = get_object_or_404(
            Birthday,
            pk=pk
        )
        form = BirthdayForm(
            instance=instance
        )
        context = {
            'form': form
        }
        if request.method == 'POST':
            instance.delete()
            return redirect('birthday:list')
        return render(
            request,
            'birthday/birthday.html',
            context
        )
'''
