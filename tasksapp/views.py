from django.shortcuts import render
from .models import Task
from django.views.generic.list import ListView
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin

class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user = self.request.user)
        context['count'] = context['tasks'].filter(completed=False).count()

        context['tasks'] = context['tasks'].order_by('completed', '-created')

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(title__icontains=search_input)

        context['search_input'] = search_input
        return context


class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'completed']
    success_url = reverse_lazy('task-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)

class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'completed']
    success_url = reverse_lazy('task-list')

class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('task-list')
