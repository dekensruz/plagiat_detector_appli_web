from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('process/<int:document_id>/', views.process_document, name='process_document'),
    path('analyze/<int:document_id>/', views.analyze_document, name='analyze_document'),
    path('results/<int:result_id>/', views.results, name='results'),
    path('documents/', views.document_list, name='document_list'),
]