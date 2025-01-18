from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_confirmation_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('', views.book_list, name='book_list'),
    path('create/', views.book_create, name='book_create'),
    path('book/<int:id>/', views.book_detail, name='book_detail'),
    path('book/<int:id>/update/', views.book_update, name='book_update'),
    path('book/<int:id>/delete/', views.book_delete, name='book_delete'),
]
