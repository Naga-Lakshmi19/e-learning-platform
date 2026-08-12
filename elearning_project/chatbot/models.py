from django.db import models

class UploadedPDF(models.Model):
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='pdfs/')
    extracted_text = models.TextField()
    

class ChatQA(models.Model):
    question = models.CharField(max_length=500)
    answer = models.TextField()

    def __str__(self):
        return self.question