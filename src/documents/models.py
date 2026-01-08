from django.db import models

# Create your models here.
from django.db import models
from pgvector.django import VectorField

class Document(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    embedding = VectorField(dimensions=384)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
