from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ListModel(models.Model):
    name=models.CharField(max_length=20,verbose_name='List name')
    date_created=models.DateField(auto_now=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class TaskModel(models.Model):
    name = models.CharField(max_length=20, verbose_name='Task name')
    list=models.ForeignKey(ListModel,on_delete=models.CASCADE,)
    date_created=models.DateField(auto_now=True,verbose_name='Date created')
    complete=models.BooleanField(default=False)
    def __str__(self):
        return self.name
