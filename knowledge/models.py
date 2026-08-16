from django.conf import settings
from django.db import models
from pgvector.django import VectorField


class KnowledgeDocument(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to="knowledge_documents/")
    document_type = models.CharField(max_length=100)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="knowledge_documents")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class DocumentChunk(models.Model):
    document = models.ForeignKey(KnowledgeDocument,on_delete=models.CASCADE,related_name="chunks")
    content = models.TextField()
    chunk_index = models.PositiveIntegerField()
    page_number = models.PositiveIntegerField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # pgvector VectorField with 384 dimensions (all-MiniLM-L6-v2 generates 384-dimensional embeddings)
    embedding = VectorField(dimensions=384, null=True, blank=True)

    def __str__(self):
        return f"{self.document.title} - Chunk {self.chunk_index}"
    
    
    