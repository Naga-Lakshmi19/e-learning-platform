from django.shortcuts import render, redirect
from .models import ContactMessage

def contact_admin(request):

    if request.method == "POST":
        ContactMessage.objects.create(
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            message=request.POST.get('message')
        )

    return render(request, 'contact.html')


def view_messages(request):

    # Only admin should see this page
    if not request.session.get('is_admin'):
        return redirect('login')

    messages = ContactMessage.objects.all().order_by('-id')

    return render(request, 'view_messages.html', {'messages': messages})