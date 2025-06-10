from django.contrib import admin
from .models import Document, PlagiarismResult

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'document_type', 'uploaded_at')
    list_filter = ('document_type', 'uploaded_at')
    search_fields = ('title',)

@admin.register(PlagiarismResult)
class PlagiarismResultAdmin(admin.ModelAdmin):
    list_display = ('document', 'created_at')
    list_filter = ('created_at',)
