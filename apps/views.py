from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView

from apps.forms import RegisterForm
from apps.models import Model


def items(request):
    context = {
        'items': Model.objects.all()
    }
    return render(request, 'index.html', context)


def add_item(request):
    if request.method == 'POST':
        Model.objects.create(
            name=request.POST.get['name'],
            image=request.FILES['image'],
            description=request.POST['description'],
            location=request.POST['location'],
            money=request.POST['money'],
        )
        return redirect('items')
    return render(request, 'add_index.html')


def delete_item(request, pk):
    Model.objects.filter(id=pk).delete()
    return redirect('items')


class RegisterFormView(FormView):
    template_name = 'profile/login.html'
    form_class = RegisterForm
    success_url = reverse_lazy('register_page')


def login_page(request):
    if request.method == 'POST':
        name = request.POST.get('username')
        password = request.POST.get('password')
        if User.objects.filter(name=name).exists():
            user = authenticate(request, name=name, password=password)
            login(request, user)
            return redirect('main_page')

    return render(request, 'profile/login.html')
