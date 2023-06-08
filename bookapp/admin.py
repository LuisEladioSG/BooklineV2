from django.contrib import admin
from django.contrib.auth.models import User
from .models import Category, Book, BookSearch, UserProfile

class UserProfileInline(admin.StackedInline):
    model = UserProfile

class UserAdmin(admin.ModelAdmin):
    inlines = [UserProfileInline]

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Category)
admin.site.register(Book)
admin.site.register(BookSearch)
