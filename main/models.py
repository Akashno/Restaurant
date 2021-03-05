from django.contrib.auth.models import User
from django.db import models


class Notifications(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    notification = models.CharField(max_length=300, null=True)
    seen = models.BooleanField(default=False, null=True)

    # date_created = models.DateTimeField(auto_now_add=True,null=True)
    class Meta:
        verbose_name_plural = "Notifications"


class Products(models.Model):
    name = models.CharField(max_length=100)
    img = models.ImageField(upload_to='pics')
    desc = models.CharField(max_length=500)
    price = models.FloatField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Products"


class Cart(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Products, null=True, on_delete=models.SET_NULL)
    count = models.IntegerField(default=1)
    total = models.IntegerField(default=0, null=True)

    def get_name(self):
        return self.product.name

    def get_price(self):
        return self.product.price

    def get_count(self):
        return self.count

    def get_total(self):
        self.total = self.count * self.product.price
        return self.total

    def update_count(self):
        self.count = self.count + 1

    def __str__(self):
        return self.product.name


class Orders(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Products, null=True, on_delete=models.SET_NULL)
    count = models.IntegerField(default=1)
    total = models.IntegerField(default=0, null=True)
    delivered = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def get_name(self):
        return self.product.name

    def get_price(self):
        return self.product.price

    def get_count(self):
        return self.count

    def get_total(self):
        self.total = self.count * self.product.price
        return self.total

    def update_count(self):
        self.count = self.count + 1

    class Meta:
        verbose_name_plural = "Orders"

    def __str__(self):
        return str(self.user) + " " + str(self.product)


class Table(models.Model):
    seats = models.IntegerField()
    reserved = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)


class Reservation(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    table = models.ForeignKey(Table, null=True, on_delete=models.SET_NULL)
    date = models.DateField(null=True)
    time = models.TimeField(null=True)

    def __str__(self):
        return str(self.user) + ":" + str(self.table.id)


class Payment(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    acnumber = models.IntegerField()
    expirem = models.IntegerField()
    expirey = models.IntegerField()
    ccv = models.IntegerField()

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name_plural = "Payment Details"
