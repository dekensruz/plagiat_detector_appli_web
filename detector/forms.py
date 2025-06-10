from django import forms
from .models import Document

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title', 'file']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Titre du document'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
        }
        
    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            file_extension = file.name.split('.')[-1].lower()
            if file_extension not in ['pdf', 'docx']:
                raise forms.ValidationError("Seuls les fichiers PDF et DOCX sont acceptés.")
            
            # Déterminer automatiquement le type de document
            self.instance.document_type = file_extension
            
        return file