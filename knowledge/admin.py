from django.contrib import admin
from .models import KnowledgeDocument, DocumentChunk


@admin.register(KnowledgeDocument)
class KnowledgeDocumentAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "document_type",
        "created_by",
        "created_at",
        "updated_at",
    )
    search_fields = ("title", "content")
    list_filter = ("document_type",)


@admin.register(DocumentChunk)
class DocumentChunkAdmin(admin.ModelAdmin):
    list_display = (
        "document",
        "chunk_index",
        "page_number",
        "created_at",
    )
    search_fields = ("content",)
    list_filter = ("document",)