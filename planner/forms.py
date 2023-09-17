from .models import Task, Label
from django.forms import ModelForm, TextInput, Textarea, ModelChoiceField
from django import forms


class TaskForm(ModelForm):

    class Meta:
        model = Task
        fields = '__all__'
        widgets = {
            "task": TextInput(attrs={'class': 'addtask_name_input',
                                     'id': 'id_task',
                                    'placeholder': 'Название задачи',
                                    'autocomplete':'off'}),
            "description": Textarea(attrs={'class': 'addtask_description_input',
                                     'placeholder': 'Описание задачи',
                                     'style': 'width: 100%;'}),
            "checkbox": False,
            "finish": forms.DateInput(attrs={"id": "airdatepicker", "class": 'addtask_date_input',
                                             'autocomplete': 'off', 'placeholder': 'Date'}),
        }


class EditTaskForm(ModelForm):
    class Meta:
        model = Task
        fields = '__all__'
        widgets = {
            "task": TextInput(attrs={'class': 'addtask_name_input',
                                    'placeholder': 'Название задачи',
                                    'autocomplete':'off'}),
            "description": Textarea(attrs={'class': 'addtask_description_input',
                                     'placeholder': 'Описание задачи'}),
            "finish": forms.DateInput(attrs={"id": "airdatepicker-2", "class": 'addtask_date_input',
                                             'autocomplete': 'off', 'placeholder': 'Date'}),
        }
