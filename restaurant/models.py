from django.contrib.auth.models import AbstractUser
from django.db import models

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

class MenuItem(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    availability = models.PositiveIntegerField(default=0)  

    def __str__(self):
        return f"{self.name} ({self.price:.2f}€) - Available: {self.availability}"

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

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} x {self.menu_item.name} for Order #{self.order.id}"

    def save(self, *args, **kwargs):
        """When creating a new OrderItem (no existing PK), reduce the menu item's availability."""
        if not self.pk:  # Only reduce stock if the object doesn't exist yet
            if self.menu_item.availability < self.quantity:
                raise ValueError("Not enough availability.")
            self.menu_item.availability -= self.quantity
            self.menu_item.save()
        super().save(*args, **kwargs)

    # def update_quantity(self, new_quantity):
    #     """
    #     Update the quantity of an existing OrderItem.
        
    #     - If increasing quantity, check stock before allowing the update.
    #     - If decreasing quantity, restore the corresponding stock.
    #     - Adjust the menu item's availability accordingly.
    #     """
    #     diff = new_quantity - self.quantity
    #     if diff > 0:
    #         if self.menu_item.availability < diff:
    #             raise ValueError("Not enough availability to increase quantity.")
    #         self.menu_item.availability -= diff
    #     else:
    #         self.menu_item.availability += abs(diff)
        
    #     self.menu_item.save()
    #     self.quantity = new_quantity
    #     self.save()

    def restore_stock_and_delete(self):
        """Return stock to menu when deleting."""
        self.menu_item.availability += self.quantity
        self.menu_item.save()
        self.delete()