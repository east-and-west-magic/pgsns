import os
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import RegisterForm
import requests
from . import status
# Create your views here.

base_url = "https://pgsoft-pguser.hf.space"
url_login = f"{base_url}/user/login"
db_token = os.getenv('db_token')
header = {
    'accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': f"Bearer {db_token}",
}


def post_to_pguser(url: str, obj: dict = None) -> dict:
    """post to pguser

    Args:
        url (str): url to post
        obj (dict, optional): designate this while post json. Defaults to None.

    Returns:
        dict: response, includes keys: status, data, msg
    """
    try:
        res = requests.post(url=url, headers=header, json=obj)
        return res.json()
    except Exception as e:
        print(f"[post_to_pguser]{type(e)}: {e}")
        return {
            "status": status.FAILURE,
            "data": {},
            "msg": "Internal Server Error",
        }


def login(request) -> HttpResponse:
    """show login page and some possible message"""
    error = request.GET.get("error", "false")
    message = request.GET.get("message", "")
    email = request.GET.get("email", "")
    context = {
        "error": error,
        "message": message,
        "email": email,
    }
    return render(request, "login.html", context)


def verify_password(request) -> HttpResponse | HttpResponseRedirect:
    """verify user's email and password"""
    context = {}
    email = request.POST.get("email").strip().lower()
    password = request.POST.get("password")
    url = f"{url_login}?email={email}&password={password}"
    res = post_to_pguser(url)
    stat = res.get("status", status.FAILURE)
    if stat == status.FAILURE:
        error = "true"
        msg = "Invalid email or password"
        url = f"../login?error={error}&message={msg}&email={email}"
        return redirect(url)
    context = {
        "email": email,
    }
    return render(request, "loggedin.html", context)


def register(request):
    if request.method == "POST":
        print("posting")
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            # upload to dataset
            return redirect("/")
    else:
        form = RegisterForm()
    return render(request, "register.html", {"form": form})
