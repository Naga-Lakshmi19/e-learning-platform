from django.shortcuts import render, redirect

def login_view(request):

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Fixed Admin Login
        if username == "admin" and password == "admin":
            request.session['is_admin'] = True
            return redirect("dashboard")
        else:
            return render(request, "login.html", {"error": "Invalid Login"})

    return render(request, "login.html")


def dashboard_view(request):

    if not request.session.get('is_admin'):
        return redirect("login")

    return render(request, "dashboard.html")


def logout_view(request):
    request.session.flush()
    return redirect("login")



from .models import Learner

def index(request):
    return render(request, 'index.html')


def register(request):

    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        Learner.objects.create(
            name=name,
            email=email,
            password=password
        )

        return redirect('user_login')

    return render(request, 'register.html')


def user_login(request):

    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = Learner.objects.filter(email=email, password=password).first()

        if user:
            request.session['user_id'] = user.id
            request.session['user_name'] = user.name
            return redirect('user_dashboard')
        else:
            return render(request, 'user_login.html', {'error': 'Invalid Login'})

    return render(request, 'user_login.html')


def user_dashboard(request):

    if not request.session.get('user_id'):
        return redirect('user_login')

    return render(request, 'user_dashboard.html')


def user_logout(request):
    request.session.flush()
    return redirect('index')


from .models import Learner

def view_users(request):

    if not request.session.get('is_admin'):
        return redirect('login')

    users = Learner.objects.all()
    return render(request, 'view_users.html', {'users': users})

def delete_user(request, user_id):

    if not request.session.get('is_admin'):
        return redirect('login')

    user = Learner.objects.get(id=user_id)
    user.delete()

    return redirect('/view-users/')