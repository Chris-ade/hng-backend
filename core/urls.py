# core/urls.py
from django.urls import path

from .views import index, hello, RegisterView, LoginView, UserView, UserOrganizationsView, SingleOrganizationView, AddUserToOrganizationView

urlpatterns = [
    path('', index),
    path('hello', hello),
    path('auth/register', RegisterView.as_view(), name='register'),
    path('auth/login', LoginView.as_view(), name='login'),
    path('users/<str:id>', UserView.as_view(), name='user_data'),
    path('organisations', UserOrganizationsView.as_view(), name='user_orgs'),
    path('organisations/<str:orgId>', SingleOrganizationView.as_view(), name='org_view'),
    path('organisations/<str:orgId>/users', AddUserToOrganizationView.as_view(), name='add_user'),
]