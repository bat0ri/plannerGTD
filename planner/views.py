from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from .models import Task, Category, Label
from .forms import TaskForm, EditTaskForm
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse



def index(request):
    tasks = Task.objects.filter(user=request.user)
    form = TaskForm(initial={'checkbox': False})
    edit = EditTaskForm()
    cat = Category.objects.all()
    labels = Label.objects.filter(user=request.user)

    category_id = request.GET.get('category')

    if category_id and category_id != "":
        # Если передан параметр категории и он не пустой, фильтруем задачи по этой категории
        tasks = tasks.filter(category_id=category_id)
    else:
        # Если категория не выбрана, включаем в результаты задачи без категории
        tasks = tasks.filter(category__isnull=True)

    return render(request, 'planner/index.html',
                  {'tasks': tasks, 'form': form, 'edit': edit, 'cat': cat, 'labels': labels})


@login_required
def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            checkbox = request.POST.get('checkbox') == 'True'
            task.checkbox = checkbox
            task.save()
            labels: object = request.POST.getlist('labels')
            task.labels.set(labels)
            return JsonResponse({'success': True})
        else:
            errors = form.errors.as_json()
            print(errors)  # Отладочное сообщение
            return JsonResponse({'success': False, 'errors': errors})
    else:
        form = TaskForm(initial={'checkbox': False})
    return render(request, 'planner/add_task.html', {'form': form})


def delete(request, task_id):
    todo = Task.objects.get(id=task_id)
    todo.delete()

    return redirect('index')

def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    category_done = Category.objects.get(name='Выполнено')
    if task.category != category_done:
        # Присвоить категорию "Выполнено"
        task.category = category_done
        task.save()
    else:
        task.delete()

    return HttpResponseRedirect(reverse('index'))

def edit_task(request, task_id):
    if request.method == 'POST':
        task = get_object_or_404(Task, id=task_id)
        task_form = EditTaskForm(request.POST, instance=task)
        if task_form.is_valid():
            task_form.save()
            labels: object = request.POST.getlist('labels-edit')
            task.labels.set(labels)
            return HttpResponse(status=200)
        else:
            errors = task_form.errors.as_json()
            return HttpResponseBadRequest(errors)
    else:
        # Handle GET requests
        pass


@csrf_exempt
@login_required
def add_label(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        name = request.POST.get('name')
        color = request.POST.get('color')
        if name:
            label = Label(name=name, color=color)
            label.user = request.user
            label.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Name is required'})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid method or request'})

@login_required
def delete_label(request, label_id):
    try:
        label = Label.objects.get(id=label_id, user=request.user)
        label.delete()
        return JsonResponse({'success': True})
    except Label.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Метка не найдена'})

