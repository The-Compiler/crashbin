from django.shortcuts import render


def home(request):
    return render(request, 'crashbin_app/home.html', {})
