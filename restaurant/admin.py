"""
This file is reserved for future admin customizations.
For example, registering models with custom forms and filters.
"""

# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from .forms import CustomUserChangeForm, CustomUserCreationForm
# from .models import User, MenuItem, Order, OrderItem

# class CustomUserAdmin(BaseUserAdmin):
#     """CustomUserAdmin needed because of the custom User model"""
#     add_form = CustomUserCreationForm
#     form = CustomUserChangeForm
#     model = User

#     list_display = ["username", "email", "role", "is_staff", "is_superuser"]
#     list_filter = ["role", "is_staff", "is_superuser"]

#     fieldsets = (
#         (None, {"fields": ("username", "email", "first_name", "last_name", "password")}),
#         ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
#         ("Role", {"fields": ("role",)}),
#         ("Important dates", {"fields": ("last_login",)}),
#     )

#     add_fieldsets = (
#         (None, {
#             "classes": ("wide",),
#             "fields": ("username", "email", "first_name", "last_name", "role", "password1", "password2", "is_staff", "is_superuser", "is_active")}
#         ),
#     )

# admin.site.register(User, CustomUserAdmin)
# admin.site.register(MenuItem)
# admin.site.register(Order)
# admin.site.register(OrderItem)