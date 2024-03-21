from django.shortcuts import render, redirect

# Create your views here.


def login(request):
    """show login page and some possible message"""
    error = request.GET.get("error", "false")
    message = request.GET.get("message", "")
    email=request.GET.get("email", "")
    context = {
        "error": error,
        "message": message,
        "email": email,
    }
    return render(request, "login.html", context)


def login_verify(request):
    context = {}
    email = request.POST.get("email").strip().lower()
    password = request.POST.get("password")
    password_confirm = request.POST.get("password_confirm")
    if password != password_confirm:
        error = "true"
        msg = "Entered passwords do not match"
        url = f"../login?error={error}&message={msg}&email={email}"
        return redirect(url)
    
    # TODO: verify 
    context = {
        "email": email,
    }

    return render(request, "loggedin.html", context)
