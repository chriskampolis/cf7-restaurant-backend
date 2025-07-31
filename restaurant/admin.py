from django.contrib import admin
from .models import User, MenuItem

# Register your models here.
admin.site.register(User)
admin.site.register(MenuItem)
# admin.site.register(Reservation)