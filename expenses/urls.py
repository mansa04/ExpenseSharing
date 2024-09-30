# expenses/urls.py
from django.urls import path
from .views import (
    create_group,
    groups_list,
    add_member,
    add_expense,
    register,
    user_login,
    user_logout,
    group_detail,
    delete_group,
)

urlpatterns = [
    path('create-group/', create_group, name='create_group'),
    path('groups/', groups_list, name='groups_list'),
    path('groups/<int:group_id>/', group_detail, name='group_detail'),
    path('groups/<int:group_id>/add-member/', add_member, name='add_member'),
    path('groups/<int:group_id>/add-expense/', add_expense, name='add_expense'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('groups/<int:id>/delete/', delete_group, name='delete_group'),
]
