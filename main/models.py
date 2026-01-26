from ast import mod
from os import name
from django.db import models
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to='categories/', null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children', null=True, blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='%(class)ss')
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    image_1 = models.ImageField(upload_to='products/', null=True, blank=True)
    image_2= models.ImageField(upload_to='products/', null=True, blank=True)
    image_3 = models.ImageField(upload_to='products/', null=True, blank=True)
    image_4 = models.ImageField(upload_to='products/', null=True, blank=True)
    image_5 = models.ImageField(upload_to='products/', null=True, blank=True)
    name = models.CharField(max_length=250, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    price = models.CharField(max_length=250, null=True, blank=True)

    
    for_dad = models.BooleanField(default=True, verbose_name="для тата")
    for_mom = models.BooleanField(default=True, verbose_name="для мами")


    is_available = models.BooleanField(default=True, verbose_name="Доступний для продажу")
    
    def __str__(self):
        return self.name
        
class To_Buy(models.Model):

    name = models.CharField(max_length=250, null=True, blank=True)
    status = models.BooleanField(default=True, verbose_name="статус")

    name_user = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    # Nova Poshta
    address_nova_poshta = models.CharField(max_length=100, null=True, blank=True)
    city_nova_poshta = models.CharField(max_length=100, null=True, blank=True)
    region_nova_poshta = models.CharField(max_length=100, null=True, blank=True)
    branch_nova_poshta = models.CharField(max_length=100, null=True, blank=True)
    # Ukrposhta
    address_ukr_poshta = models.CharField(max_length=100, null=True, blank=True)
    city_ukr_poshta = models.CharField(max_length=100, null=True, blank=True)
    region_ukr_poshta = models.CharField(max_length=100, null=True, blank=True)
    inbex_ukr_poshta = models.CharField(max_length=100, null=True, blank=True)

    
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Загальна ціна", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення", null=True, blank=True)
    def __str__(self):
        return f"Замовлення від {self.name_user} (ID: {self.id})"

        
class To_Buy_Product(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='to_buy_products', null=True, blank=True)
    data_user = models.ForeignKey('Save_user_data', on_delete=models.CASCADE, related_name='to_buy_products', null=True, blank=True)
    to_buy = models.ForeignKey('To_Buy', on_delete=models.CASCADE, related_name='to_buy_products')
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='to_buy_products', null=True, blank=True)

    name = models.CharField(max_length=250, null=True, blank=True)
    price = models.CharField(max_length=250, null=True, blank=True)
    number = models.PositiveIntegerField(default=1, verbose_name="Кількість товару")
    status = models.BooleanField(default=True, verbose_name="статус")

    name_user = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    # Nova Poshta
    address_nova_poshta = models.CharField(max_length=100, null=True, blank=True)
    city_nova_poshta = models.CharField(max_length=100, null=True, blank=True)
    region_nova_poshta = models.CharField(max_length=100, null=True, blank=True)
    branch_nova_poshta = models.CharField(max_length=100, null=True, blank=True)
    # Ukrposhta
    address_ukr_poshta = models.CharField(max_length=100, null=True, blank=True)
    city_ukr_poshta = models.CharField(max_length=100, null=True, blank=True)
    region_ukr_poshta = models.CharField(max_length=100, null=True, blank=True)
    inbex_ukr_poshta = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")
    
    def __str__(self):
        if self.data_user and self.data_user.name:
            return f"Замовлення від {self.data_user.name} (ID: {self.id})"
        elif self.user:
            return f"Замовлення від {self.user.username} (ID: {self.id})"
        else:
            return f"Замовлення #{self.id}"

class Save_user_data(models.Model):
    # User
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='save_user_data', null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    # Nova Poshta
    address_nova_poshta = models.CharField(max_length=100, null=True, blank=True)
    city_nova_poshta = models.CharField(max_length=100, null=True, blank=True)
    region_nova_poshta = models.CharField(max_length=100, null=True, blank=True)
    branch_nova_poshta = models.CharField(max_length=100, null=True, blank=True)
    # Ukrposhta
    address_ukr_poshta = models.CharField(max_length=100, null=True, blank=True)
    city_ukr_poshta = models.CharField(max_length=100, null=True, blank=True)
    region_ukr_poshta = models.CharField(max_length=100, null=True, blank=True)
    inbex_ukr_poshta = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        if self.name:
            return self.name
        elif self.user:
            return f"Дані користувача {self.user.username} (ID: {self.id})"
        else:
            return f"Дані користувача #{self.id}"
            
class Comment(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    product = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment #{self.id} for {self.product}'