from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Book
from .forms import BookForm
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_protect


# Страница регистрации
def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('book_list')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

# Страница входа
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('book_list')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# Выход из системы
@csrf_protect
def logout_confirmation_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')  # Перенаправление на страницу входа
    return render(request, 'logout_confirmation.html')  # Показать страницу подтверждения


# Список книг
@login_required(login_url='/register/')
def book_list(request):
    books = Book.objects.all().order_by('-id')
    paginator = Paginator(books, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'book_list.html', {'page_obj': page_obj})


# Создание книги
@login_required
def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            book.user = request.user  # Установить текущего пользователя как автора
            book.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'book_form.html', {'form': form})

# Просмотр книги
def book_detail(request, id):
    book = Book.objects.get(id=id)
    return render(request, 'book_detail.html', {'book': book})

# Редактирование книги
@login_required
def book_update(request, id):
    book = get_object_or_404(Book, id=id)

    # Проверяем, что текущий пользователь является автором книги
    if book.user != request.user:
        return redirect('book_list')

    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'book_form.html', {'form': form, 'book': book})

# Удаление книги
@login_required
def book_delete(request, id):
    book = get_object_or_404(Book, id=id)

    # Проверяем, что текущий пользователь является автором книги
    if book.user != request.user:
        return redirect('book_list')

    if request.method == 'POST':
        book.delete()
        return redirect('book_list')

    return render(request, 'book_confirm_delete.html', {'book': book})
