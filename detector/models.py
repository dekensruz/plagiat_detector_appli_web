from django.db import models
from django.utils import timezone

class Document(models.Model):
    DOCUMENT_TYPES = (
        ('pdf', 'PDF'),
        ('docx', 'DOCX'),
    )
    
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='documents/')
    document_type = models.CharField(max_length=4, choices=DOCUMENT_TYPES)
    uploaded_at = models.DateTimeField(default=timezone.now)
    extracted_text = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.title

class PlagiarismResult(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='plagiarism_results')
    created_at = models.DateTimeField(default=timezone.now)
    result_json = models.JSONField(blank=True, null=True)
    
    def __str__(self):
        return f"Résultat pour {self.document.title}"
