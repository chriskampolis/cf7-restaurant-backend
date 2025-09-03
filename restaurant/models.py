from django.contrib.auth.models import AbstractUser
from django.db import models

# Extend Django's built-in user model to support custom roles (manager/employee).
class User(AbstractUser):
    ROLE_CHOICES = (
        ('manager', 'Manager'),
        ('employee', 'Employee'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='employee')

    def is_manager(self):
        return self.role == 'manager'
    
    def __str__(self):
        return f"{self.username} ({self.role})"

# Menu items (dishes and drinks) that employees/managers can order.
class MenuItem(models.Model):
    class Category(models.TextChoices):
        APPETIZER = "APPETIZER", "Appetizer"
        MAIN = "MAIN", "Main Dish"
        DESSERT = "DESSERT", "Dessert"
        DRINK = "DRINK", "Drink"

    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    availability = models.PositiveIntegerField(default=0)  
    category = models.CharField(
        max_length=20,
        choices=Category.choices,
        default=Category.MAIN,
    )

    def __str__(self):
        return f"{self.name} ({self.price:.2f}€) - Available: {self.availability} ({self.category})"

# Represents a single order placed at a specific table.
class Order(models.Model):
    STATUS_CHOICES = [
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]

    table_number = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_progress')
    placed_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Order # {self.id} - Table {self.table_number} - {self.status} - placed by {self.placed_by.username} at {self.created_at.strftime('%Y-%m-%d %H:%M')}"
    
    @property
    def total_price(self):
        """Calculate the total price of all items in the order."""
        return sum(item.menu_item.price * item.quantity for item in self.items.all())

# Links a MenuItem to an Order (e.g. 2x Burger in Order #5).
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} x {self.menu_item.name} for Order #{self.order.id}"

    def save(self, *args, **kwargs):
        """
        When creating a new OrderItem (no existing PK), reduce the menu item's availability.
        (Prevents overselling if stock < requested quantity).
        """
        if not self.pk:  # Only reduce stock if the object doesn't exist yet    
            if self.menu_item.availability < self.quantity:
                raise ValueError("Not enough availability.")
            self.menu_item.availability -= self.quantity
            self.menu_item.save()
        super().save(*args, **kwargs)

    def restore_stock_and_delete(self):
        """If an item is removed from an order, return its stock."""
        self.menu_item.availability += self.quantity
        self.menu_item.save()
        self.delete()