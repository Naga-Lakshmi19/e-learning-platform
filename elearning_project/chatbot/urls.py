from django.urls import path
from .views import *

urlpatterns = [
    path('chat/', curriculum_chat),
    path('upload-pdf/', upload_pdf),
    path('ask-pdf/', ask_pdf),
    path('add-qa/', add_qa, name="add_qa"),
]