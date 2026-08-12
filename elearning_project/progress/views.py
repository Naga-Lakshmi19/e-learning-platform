from django.shortcuts import redirect
from .models import LessonProgress
from courses.models import Lesson

def complete_lesson(request, lesson_id):

    lesson = Lesson.objects.get(id=lesson_id)

    LessonProgress.objects.get_or_create(
        lesson=lesson,
        completed=True
    )

    return redirect(f'/learn/{lesson.subject.id}/')