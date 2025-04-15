from django.shortcuts import render
from .models import Task
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


@login_required
def tasks(request):
    tasks = Task.objects.all()
    return render(request, 'tasks/tasks.html', 
                  {'tasks': tasks})


