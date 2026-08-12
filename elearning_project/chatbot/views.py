from django.shortcuts import render, redirect
from courses.models import Lesson
import PyPDF2
from .models import UploadedPDF
from .models import ChatQA
from courses.models import Lesson

def curriculum_chat(request):

    answer = None
    question = None

    if request.method == "POST":
        question = request.POST.get('question')

        if question:

            # 🔹 1. Check Admin Added Questions First
            qa = ChatQA.objects.filter(question__icontains=question).first()

            if qa:
                answer = qa.answer

            else:
                # 🔹 2. Search Inside Lessons Content
                lesson = Lesson.objects.filter(content__icontains=question).first()

                if lesson:
                    answer = lesson.content
                else:
                    answer = "Sorry, this question is not available in the system."

    return render(request, 'chat.html', {
        'answer': answer,
        'question': question
    })


import PyPDF2
from django.shortcuts import render, redirect
from .models import UploadedPDF, ChatQA


def upload_pdf(request):

    message = None

    if request.method == "POST":

        title = request.POST.get('title')
        file = request.FILES.get('file')

        if not file:
            message = "Please upload a file."

        elif not file.name.endswith(".pdf"):
            message = "Only PDF files are allowed."

        else:
            try:

                reader = PyPDF2.PdfReader(file)

                text = ""

                for page in reader.pages:
                    extracted = page.extract_text()

                    if extracted:
                        text += extracted + "\n"

                UploadedPDF.objects.create(
                    title=title,
                    file=file,
                    extracted_text=text
                )

                message = "PDF uploaded successfully."

            except Exception:
                message = "Invalid or corrupted PDF file."

    return render(request, 'upload_pdf.html', {"message": message})


# ------------------------------------------


def ask_pdf(request):

    answer = None

    if request.method == "POST":

        question = request.POST.get('question')

        pdf = UploadedPDF.objects.last()

        if not pdf:
            answer = "No PDF uploaded yet."

        elif not pdf.extracted_text:
            answer = "No readable text found in this PDF."

        else:

            text = pdf.extracted_text

            paragraphs = text.split("\n")

            keywords = question.lower().split()

            best_match = None
            max_score = 0

            for para in paragraphs:

                score = 0

                for word in keywords:

                    if word in para.lower():
                        score += 1

                if score > max_score:
                    max_score = score
                    best_match = para

            if best_match and max_score > 0:
                answer = best_match
            else:
                answer = "Relevant content not found in PDF."

    return render(request, 'ask_pdf.html', {"answer": answer})


# ------------------------------------------


def add_qa(request):

    if not request.session.get('is_admin'):
        return redirect('login')

    message = None

    if request.method == "POST":

        question = request.POST.get('question')
        answer = request.POST.get('answer')

        if question and answer:
            ChatQA.objects.create(
                question=question,
                answer=answer
            )
            message = "Knowledge added successfully."

    return render(request, 'add_qa.html', {"message": message})