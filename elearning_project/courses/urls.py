from django.urls import path
from .views import *

urlpatterns = [
    path('add-subject/', add_subject, name="add_subject"),
    path('subjects/', view_subjects, name="view_subjects"),
    path('add-lesson/', add_lesson, name="add_lesson"),
    path('lessons/', view_lessons, name="view_lessons"),
    path('learn/', learn_subjects, name="learn_subjects"),
    path('learn/<int:subject_id>/', learn_lessons, name="learn_lessons"),
    path('lesson/<int:lesson_id>/', read_lesson, name="read_lesson"),
    path('search/', search_lessons, name="search_lessons"),
    path('bookmark/<int:lesson_id>/', add_bookmark),
    path('bookmarks/', view_bookmarks),
    path('history/', view_history),
    path('delete-subject/<int:subject_id>/', delete_subject),
    path('delete-lesson/<int:lesson_id>/', delete_lesson),
    path('learn/<int:subject_id>/', subject_lessons)
]