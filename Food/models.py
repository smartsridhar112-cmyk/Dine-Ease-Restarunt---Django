from django.db import models
from django.conf import settings

class Category(models.Model):

    food_image= models.ImageField(upload_to='images/', null=True)
    food_name =models.CharField(max_length=50, null=True)
    food_price = models.FloatField(default=0)
    food_availabity = models.BooleanField(default=False)
    category_choice =[
        ("veg","veg"),
        ("non-veg","non-veg")
    ]
    categories = models.CharField(max_length=20, choices=category_choice ,null=True,blank=True)

    food_choice=[
        ("Soup","Soup"),
        ("Pizza","Pizza"),
        ("Burger","Burger"),
        ("Rolls","Rolls"),
        ("Cakes","Cakes"),
        ("Drinks","Drinks"),
        ("Milk Shake","Milk Shake"),
        ("Fride Rice","Fride Rice"),
        ("Fride Noodles","Fride Noodles"),
        ("Sandwich","Sandwich"),
        ("Ice Cream","Ice Cream"),
        ("Variety Rice","Variety Rice"),
    ]
    food_category = models.CharField(max_length=30, choices=food_choice,null=True,blank=True)

    def __str__(self):
        return self.food_name


class Cart(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    food_name=models.CharField(max_length=50,null=True)
    quantity= models.FloatField(default=1)
    amount = models.DecimalField(max_digits=5,decimal_places=2)

    def __str__(self):
        return self.category.food_name
    

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True,blank=True)
    category= models.ForeignKey(Category,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1,null=True)
    amount = models.DecimalField(max_digits=5,decimal_places=2)
    status = models.CharField(max_length=20,default="pending")
    payment_id= models.CharField(max_length=50,blank=True,null=True)

    def __str__(self):
        return self.category.food_name


class MyOrders(models.Model):
    category=models.ForeignKey(Category,on_delete=models.PROTECT)
    food_name=models.CharField(max_length=50,null=True)
    order= models.ForeignKey(Order,on_delete=models.CASCADE)
    datetime= models.DateTimeField(auto_now_add=True)
    cart=models.ForeignKey(Cart,on_delete=models.PROTECT,null=True)
    amount = models.CharField(max_length=20,default=0,null=True)

    def __str__(self):
        return self.category.food_name