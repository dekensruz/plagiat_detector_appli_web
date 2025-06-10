from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.conf import settings
import os

from .models import Document, PlagiarismResult
from .forms import DocumentForm
from .utils import extract_text, check_plagiarism

def home(request):
    """Page d'accueil avec le formulaire d'upload"""
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save()
            return redirect('process_document', document_id=document.id)
    else:
        form = DocumentForm()
    
    return render(request, 'detector/home.html', {'form': form})

def process_document(request, document_id):
    """Traitement du document et extraction du texte"""
    document = get_object_or_404(Document, id=document_id)
    
    # Chemin complet du fichier
    file_path = os.path.join(settings.MEDIA_ROOT, str(document.file))
    
    # Extraction du texte
    extracted_text = extract_text(file_path, document.document_type)
    document.extracted_text = extracted_text
    document.save()
    
    return redirect('analyze_document', document_id=document.id)

def analyze_document(request, document_id):
    """Analyse du document pour détecter le plagiat"""
    document = get_object_or_404(Document, id=document_id)
    
    if not document.extracted_text:
        messages.error(request, "Aucun texte n'a été extrait du document.")
        return redirect('home')
    
    # Vérification du plagiat
    result = check_plagiarism(document.extracted_text)
    
    # Enregistrement des résultats
    plagiarism_result = PlagiarismResult.objects.create(
        document=document,
        result_json=result
    )
    
    return redirect('results', result_id=plagiarism_result.id)

def results(request, result_id):
    """Affichage des résultats de l'analyse"""
    result = get_object_or_404(PlagiarismResult, id=result_id)
    document = result.document
    
    context = {
        'document': document,
        'result': result,
        'analysis': result.result_json.get('analysis', ''),
        'success': result.result_json.get('success', False),
    }
    
    return render(request, 'detector/results.html', context)

def document_list(request):
    """Liste des documents analysés"""
    documents = Document.objects.all().order_by('-uploaded_at')
    return render(request, 'detector/document_list.html', {'documents': documents})
