from django.db import models

class Learner(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    


class Subject(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True
    )

    description = models.CharField(
        max_length=300
    )

    def __str__(self):
        return self.name