from django.db import models

class Task(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('in_progress', 'В работе'),
        ('done', 'Завершена'),
    ]

    name = models.CharField(max_length=200, verbose_name='Наименование')
    parent_task = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Родительская задача')
    executor = models.ForeignKey('employees.Employee', on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks', verbose_name='Исполнитель')
    deadline = models.DateField(verbose_name='Срок')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name='Статус')

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

    def __str__(self):
        return self.name
