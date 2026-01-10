from django.contrib.auth.models import User
from django.db import models

from authors.models import Author


# Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    counter = models.IntegerField(default=0)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['name', 'user'], name='unique_tag')]

    def __str__(self):
        return self.name


class Quote(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    quote = models.TextField(max_length=250)
    tags = models.ManyToManyField(Tag)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f"{self.quote}, {self.tags.all()}"
