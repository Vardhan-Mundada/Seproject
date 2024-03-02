from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    budget_limit = models.DecimalField(max_digits=10, decimal_places=2, default=True, null=False )

    def __str__(self):
        return self.name

