from django.shortcuts import render, redirect
from .models import Subject, Lesson

def add_subject(request):

    if not request.session.get('is_admin'):
        return redirect('login')

    error = None
    success = None

    if request.method == "POST":
        name = request.POST.get('name')
        description = request.POST.get('description')

        # Check if subject already exists
        if Subject.objects.filter(name__iexact=name).exists():
            error = "Subject already exists."

        else:
            Subject.objects.create(
                name=name,
                description=description
            )
            success = "Subject added successfully."

    return render(request, 'add_subject.html', {
        'error': error,
        'success': success
    })


def view_subjects(request):

    if not request.session.get('is_admin'):
        return redirect('login')

    subjects = Subject.objects.all()
    return render(request, 'view_subjects.html', {'subjects': subjects})


def add_lesson(request):

    if not request.session.get('is_admin'):
        return redirect('login')

    subjects = Subject.objects.all()
    error = None
    success = None

    if request.method == "POST":

        subject_id = request.POST.get('subject_id')
        title = request.POST.get('title')
        content = request.POST.get('content')
        order = request.POST.get('order')
        image = request.FILES.get('image')

        subject = Subject.objects.get(id=subject_id)

        # Default order if empty
        if not order:
            order = 1
        else:
            order = int(order)

        # Check duplicate lesson in same subject
        if Lesson.objects.filter(subject=subject, title__iexact=title).exists():
            error = "This lesson already exists for this subject."

        else:
            Lesson.objects.create(
                subject=subject,
                title=title,
                content=content,
                order=order,
                image=image
            )

            success = "Lesson added successfully."

    return render(request, 'add_lesson.html', {
        'subjects': subjects,
        'error': error,
        'success': success
    })


def view_lessons(request):

    if not request.session.get('is_admin'):
        return redirect('login')

    lessons = Lesson.objects.all().order_by('order')
    return render(request, 'view_lessons.html', {'lessons': lessons})


def learn_subjects(request):
    subjects = Subject.objects.all()
    return render(request, 'learn_subjects.html', {'subjects': subjects})


def learn_lessons(request, subject_id):
    subject = Subject.objects.get(id=subject_id)
    lessons = Lesson.objects.filter(subject=subject).order_by('order')

    return render(request, 'learn_lessons.html', {
        'subject': subject,
        'lessons': lessons
    })


from django.shortcuts import render, redirect, get_object_or_404
from .models import Lesson, History

def read_lesson(request, lesson_id):

    # 🔐 Check user login
    if not request.session.get('user_id'):
        return redirect('user_login')

    # 📘 Get lesson safely (avoids crash if wrong ID)
    lesson = get_object_or_404(Lesson, id=lesson_id)

    # 📝 Save to history (only if user exists)
    user_id = request.session.get('user_id')
    if user_id:
        History.objects.create(user_id=user_id, lesson=lesson)

    return render(request, 'read_lesson.html', {'lesson': lesson})


from progress.models import LessonProgress

def learn_lessons(request, subject_id):
    subject = Subject.objects.get(id=subject_id)
    lessons = Lesson.objects.filter(subject=subject).order_by('order')

    total = lessons.count()
    completed = LessonProgress.objects.filter(lesson__in=lessons).count()

    progress_percent = 0
    if total > 0:
        progress_percent = int((completed / total) * 100)

    return render(request, 'learn_lessons.html', {
        'subject': subject,
        'lessons': lessons,
        'progress_percent': progress_percent
    })
    

def search_lessons(request):

    query = request.GET.get('q')
    results = None

    if query:
        results = Lesson.objects.filter(title__icontains=query)

    return render(request, 'search.html', {'results': results})


from .models import Bookmark

def add_bookmark(request, lesson_id):

    user_id = request.session.get('user_id')

    if user_id:
        Bookmark.objects.get_or_create(user_id=user_id, lesson_id=lesson_id)

    return redirect(f'/lesson/{lesson_id}/')


def view_bookmarks(request):

    user_id = request.session.get('user_id')
    bookmarks = Bookmark.objects.filter(user_id=user_id)

    return render(request, 'bookmarks.html', {'bookmarks': bookmarks})


def view_history(request):
    user_id = request.session.get('user_id')
    history = History.objects.filter(user_id=user_id).order_by('-viewed_at')

    return render(request, 'history.html', {'history': history})

from django.shortcuts import redirect, get_object_or_404
from .models import Subject

def delete_subject(request, subject_id):

    if not request.session.get('is_admin'):
        return redirect('login')

    subject = get_object_or_404(Subject, id=subject_id)
    subject.delete()

    return redirect('/subjects/')

from .models import Lesson

def delete_lesson(request, lesson_id):

    if not request.session.get('is_admin'):
        return redirect('login')

    lesson = get_object_or_404(Lesson, id=lesson_id)
    lesson.delete()

    return redirect('/lessons/')


def subject_lessons(request, subject_id):

    subject = Subject.objects.get(id=subject_id)

    lessons = Lesson.objects.filter(subject=subject)

    return render(request, 'learn_lessons.html', {
        'subject': subject,
        'lessons': lessons
    })