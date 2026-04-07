from django.db import models
from user_app.models import AppUser

# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=75)
    due_date = models.DateField(null=True, blank=True)
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='tasks')

    def __str__(self):
        return f"{self.title}"