from .views import InteractWithPdf
from django.urls import path, include

urlpatterns = [
    path('', InteractWithPdf.as_view(), name='input_content'),
] 

