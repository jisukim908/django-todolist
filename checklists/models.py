from django.db import models
from users.models import User

# Create your models here.
class Todolist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_complete = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.title} | {self.user} | {self.is_complete}'
    
    