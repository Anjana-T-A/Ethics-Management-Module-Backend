from django.contrib.auth.models import User
from django.db import models

DEPARTMENT_CHOICES = [
    ("Faculty of Arts, Humanities and Social Sciences", "Faculty of Arts, Humanities and Social Sciences"),
    ("Faculty of Education and Health Sciences", "Faculty of Education and Health Sciences"),
    ("Kemmy Business School", "Kemmy Business School"),
    ("Faculty of Science and Engineering", "Faculty of Science and Engineering"),
    ("Irish World Academy of Music and Dance", "Irish World Academy of Music and Dance"),
]

class Supervisor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,default="")
    department = models.CharField(max_length=100, choices=DEPARTMENT_CHOICES)

    def __str__(self):
        return self.user.username

class Reviewer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,default="")
    department = models.CharField(max_length=100, choices=DEPARTMENT_CHOICES)

    def __str__(self):
        return self.user.username

