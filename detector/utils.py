import os
import PyPDF2
import docx
import google.generativeai as genai
from django.conf import settings

# Configuration de l'API Gemini
GEMINI_API_KEY = 'AIzaSyCvKY6DG2I9VXasm0AwDstk0FAWFWbSwqI'
genai.configure(api_key=GEMINI_API_KEY)

def extract_text_from_pdf(file_path):
    """Extraire le texte d'un fichier PDF"""
    text = ""
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text() + "\n"
    except Exception as e:
        text = f"Erreur lors de l'extraction du texte: {str(e)}"
    return text

def extract_text_from_docx(file_path):
    """Extraire le texte d'un fichier DOCX"""
    text = ""
    try:
        doc = docx.Document(file_path)
        for para in doc.paragraphs:
            text += para.text + "\n"
    except Exception as e:
        text = f"Erreur lors de l'extraction du texte: {str(e)}"
    return text

def extract_text(file_path, document_type):
    """Extraire le texte d'un fichier en fonction de son type"""
    if document_type == 'pdf':
        return extract_text_from_pdf(file_path)
    elif document_type == 'docx':
        return extract_text_from_docx(file_path)
    else:
        return "Type de document non pris en charge"

def check_plagiarism(text):
    """Vérifier le plagiat en utilisant l'API Gemini"""
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"""Analyse le texte suivant et identifie les passages qui pourraient être plagiés ou très similaires à des sources existantes. 
        Fournis une analyse détaillée avec:
        1. Les passages suspects
        2. Le pourcentage approximatif de contenu original
        3. Des recommandations pour améliorer l'originalité
        
        Texte à analyser:
        {text}
        """
        
        response = model.generate_content(prompt)
        
        result = {
            'analysis': response.text,
            'success': True
        }
        
        return result
    except Exception as e:
        return {
            'analysis': f"Erreur lors de l'analyse: {str(e)}",
            'success': False
        }