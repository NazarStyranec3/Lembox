from django.contrib import admin
# Register your models here.
from .models import Category, Product, To_Buy_Product, To_Buy, Save_user_data, Comment

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(To_Buy)
admin.site.register(To_Buy_Product)
admin.site.register(Save_user_data)
admin.site.register(Comment)