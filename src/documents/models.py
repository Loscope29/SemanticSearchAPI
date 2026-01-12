from django.db import models

# Create your models here.
from django.db import models
from pgvector.django import VectorField

class Document(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to="documents/")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class DocumentChunk(models.Model):
    document = models.ForeignKey(
        Document,
        related_name="chunks",
        on_delete=models.CASCADE
    )
    content = models.TextField()
    embedding = VectorField(dimensions=384)
    chunk_index = models.IntegerField()

    def __str__(self):
        return f"{self.document.title} - chunk {self.chunk_index}"

