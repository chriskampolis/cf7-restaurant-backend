from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import User, MenuItem, Order, OrderItem

class CustomUserAdmin(BaseUserAdmin):
    """CustomUserAdmin needed because of the custom User model"""
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User

    list_display = ["username", "email", "role", "is_staff", "is_superuser"]
    list_filter = ["role", "is_staff", "is_superuser"]

    fieldsets = (
        (None, {"fields": ("username", "email", "first_name", "last_name", "password")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Role", {"fields": ("role",)}),
        ("Important dates", {"fields": ("last_login",)}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "first_name", "last_name", "role", "password1", "password2", "is_staff", "is_superuser", "is_active")}
        ),
    )
     

# Improve display of Order and OrderItem in admin page

# class OrderItemInline(admin.TabularInline):
#     model = OrderItem
#     extra = 0

# @admin.register(Order)
# class OrderAdmin(admin.ModelAdmin):
#     list_display = ('id', 'table_number', 'placed_by', 'created_at')
#     inlines = [OrderItemInline]

# @admin.register(OrderItem)
# class OrderItemAdmin(admin.ModelAdmin):
#     list_display = ('order', 'menu_item', 'quantity')

admin.site.register(User, CustomUserAdmin)
admin.site.register(MenuItem)
admin.site.register(Order)
admin.site.register(OrderItem)