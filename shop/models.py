from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=50)
    category = models.CharField(max_length=50, default='',blank=True)
    sub_category = models.CharField(max_length=50, default='',blank=True)
    price = models.IntegerField(default=0)
    product_image = models.ImageField(upload_to='images/product_images/' ,null=True,blank=True,default='images/cute.jfif')
    desc = models.CharField(max_length=300)
    pub_date = models.DateField()

    def __str__(self):
        return self.product_name

class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE) ## many-to-one relationship
    product_name = models.ForeignKey(Product,on_delete=models.PROTECT) ## if product added in chart then product cannot delete
    quantity = models.IntegerField(default=1)
    add_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        product_name = str(self.product_name)
        return product_name

class Address(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE) ## many-to-one relationship
    name = models.CharField(max_length=50,default='',blank=True)
    email = models.EmailField(default='',blank=True)
    address = models.TextField(max_length=1000)
    phone_number = models.CharField(max_length=12,default='')
    city = models.CharField(max_length=50,default='')
    state = models.CharField(max_length=30,default='')
    zip = models.CharField(default='', max_length=6)

    def __str__(self):
        user = str(self.user)
        return user

    class Meta:
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'

STATUS_CHOICES = (
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('On The Way','On The Way'),
    ('Delivered','Delivered'),
    ('Cancel','Cancel'),
    ('Pending','Pending')
)

class Order(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE) ## many-to-one relationship
    product_count = models.IntegerField()
    total_amount = models.IntegerField()
    order_date = models.DateTimeField(blank=True,null=True)
    status = models.CharField(max_length=50,choices=STATUS_CHOICES,default='Pending')

    
    

class Ordered_Product(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField()

class Ordered_Address(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE) ## many-to-one relationship
    name = models.CharField(max_length=50,default='',blank=True)
    email = models.EmailField(default='',blank=True)
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    address = models.TextField(max_length=1000)
    phone_number = models.CharField(max_length=12,default='')
    city = models.CharField(max_length=50,default='')
    state = models.CharField(max_length=30,default='')
    zip = models.CharField(default='', max_length=6)