from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from colorfield.fields import ColorField
from django.contrib.auth.models import User


class Label(models.Model):
    name = models.CharField(max_length=255)
    color = models.CharField(max_length=7, default="#000000")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255)
    is_project = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    finish = models.DateField(blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now, blank=True)
    labels = models.ManyToManyField(Label, related_name='tasks', blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Task(models.Model):
    task = models.CharField('task', max_length=50)
    description = models.TextField('description', blank=True)
    checkbox = models.BooleanField('', default=False, null=True)
    finish = models.DateField(blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    priority = models.IntegerField(blank=True, null=False, default=1, validators=[MinValueValidator(1), MaxValueValidator(4)])
    project = models.ForeignKey(Project, on_delete=models.CASCADE, blank=True, null=True)
    labels = models.ManyToManyField(Label, related_name='projects', blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def add_to_project(self, project):
        self.project = project
        self.save()

    def save(self, *args, **kwargs):
        # Проверяем, является ли выбранная категория проектом
        if self.category and self.category.is_project:
            # Если выбранная категория является проектом, сохраняем только проект
            project = Project.objects.create(name=self.task, description=self.description, finish=self.finish)
            project.save()
            self.project = project
        else:
            # Если выбранная категория не является проектом, сохраняем задачу и проект (если он задан)
            super().save(*args, **kwargs)
            if self.project:
                self.project.save()

    def __str__(self):
        return self.task
