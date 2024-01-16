from django.urls import path

from apps.views import RegisterFormView
from apps.views import items, add_item, delete_item, login_page

urlpatterns = [
    path('', items, name='items'),
    path('add-item', add_item, name='add-item'),
    path('delete-item', delete_item, name='delete-item'),
    path('login', login_page, name='login_page'),
    path('register', RegisterFormView(), name='register_page')
]
