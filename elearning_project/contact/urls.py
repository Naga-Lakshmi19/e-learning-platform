from django.urls import path
from .views import *

urlpatterns = [
    path('contact/', contact_admin, name='contact'),
    path('admin-messages/', view_messages, name='view_messages'),
]