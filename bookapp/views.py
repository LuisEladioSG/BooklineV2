from django.shortcuts import render, redirect, reverse
from .models import Book, Category, UserProfile
from  .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


def home(request):
    if request.user.is_authenticated:
        if hasattr(request.user, 'userprofile') and request.user.userprofile.premium:
            premium_books = Book.objects.filter(premium=True)
        else:
            premium_books = None
    else:
        premium_books = None

    recommended_books = Book.objects.filter(recommended_books=True)
    fiction_books = Book.objects.filter(fiction_books=True)
    business_books = Book.objects.filter(business_books=True)

    return render(request, 'home.html', {
        'recommended_books': recommended_books,
        'business_books': business_books,
        'fiction_books': fiction_books,
        'premium_books': premium_books
    })

@login_required(login_url='login')
def all_books(request):
    books = Book.objects.all()
    return render(request, 'all_books.html', {'books':books})


@login_required(login_url='login')
def premium_books(request):
    books = Book.objects.filter(premium=True)
    return render(request, 'all_books.html', {'books': books})


def category_detail(request, slug):
    category = Category.objects.get(slug = slug)
    return render(request, 'genre_detail.html', {'category': category})

@login_required(login_url='login')
def book_detail(request, slug):
    book = Book.objects.get(slug=slug)
    book_category = book.category.first()

    if book.premium and not request.user.userprofile.premium:
        return redirect(reverse('premium_error'))

    similar_books = Book.objects.filter(category__name__startswith=book_category)    
    return render(request, 'book_detail.html', {'book': book, 'similar_books': similar_books})

def premium_error(request):
    return render(request, 'error.html')

@login_required(login_url='login')
def search_book(request):
    if request.user.userprofile.premium:
        searched_books = Book.objects.filter(title__icontains=request.POST.get('name_of_book'), premium=True)
    else:
        searched_books = Book.objects.filter(title__icontains=request.POST.get('name_of_book'))
    return render(request, 'search_book.html', {'searched_books': searched_books})

def register_page(request):
    register_form = CreateUserForm()
    if request.method == 'POST':
        register_form = CreateUserForm(request.POST)
        if register_form.is_valid():
            user = register_form.save()  # Guarda el usuario registrado
            UserProfile.objects.create(user=user, premium=False)  # Crea el perfil de usuario
            messages.info(request, "Account Created Successfully!")
            return redirect('login')
    return render(request, 'register.html', {'register_form': register_form})

def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password1')
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, "Invalid Credentials")
        
    
    return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    return redirect('home')

# Code for ChatGPT integration
# @login_required(login_url='login')
# def book_detail(request, slug):
#     book = Book.objects.get(slug=slug)
#     description = generate_book_description(book.title)
#     book_category = book.category.first()
#     similar_books = Book.objects.filter(category__name__startswith=book_category)    
#     return render(request, 'book_detail.html', {'book': book, 'description': description, 'similar_books': similar_books})
