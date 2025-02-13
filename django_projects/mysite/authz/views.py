from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from django.urls import reverse
from django.utils.http import urlencode
from django.http import HttpResponse

class OpenView(View):
    def get(self, request):
        return render(request, 'authz/main.html')

class ApereoView(View):
    def get(self, request):
        return render(request, 'authz/main.html')

class ManualProtect(View):
    def get(self, request):
        if not request.user.is_authenticated:
            login_url = reverse('authz:login') + '?' + urlencode({'next': request.path})
            return redirect(login_url)
        return render(request, 'authz/main.html')

class ProtectView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'authz/main.html')

class DumpPython(View):
    def get(self, request):
        resp = "<pre>\nUser Data in Python:\n\n"
        resp += "Login URL: " + reverse('authz:login') + "\n"
        resp += "Logout URL: " + reverse('authz:logout') + "\n\n"
        
        if request.user.is_authenticated:
            resp += "User: " + request.user.username + "\n"
            resp += "Email: " + request.user.email + "\n"
        else:
            resp += "User is not logged in\n"

        resp += "\n</pre>\n"
        resp += """<a href="/authz">Go back</a>"""
        return HttpResponse(resp)

# Custom Logout View to Handle Both GET and POST Requests
class CustomLogoutView(View):
    def post(self, request):
        logout(request)
        return redirect(reverse('authz:open'))  # Redirect to the homepage after logout
    
    def get(self, request):
        return HttpResponse("Logout must be a POST request", status=405)
