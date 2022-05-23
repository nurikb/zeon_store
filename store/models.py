from django.db import models

from slugify import slugify


class Category(models.Model):
     name = models.CharField(max_length=100)
     slug = models.SlugField(unique=True)

     def save(self, *args, **kwargs):
          self.slug = slugify(self.name)
          super(Product, self).save(*args, **kwargs)

     def __str__(self):
          return self.name


class Collection(models.Model):
     name = models.CharField(max_length=100)
     slug = models.SlugField(unique=True)

     def save(self, *args, **kwargs):
          self.slug = slugify(self.name)
          super(Collection, self).save(*args, **kwargs)

     def __str__(self):
          return self.name


class Product(models.Model):
     name = models.CharField(max_length=100)
     price = models.DecimalField(max_digits=6, decimal_places=3)
     created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
     modified_at = models.DateTimeField(auto_now=True, verbose_name='Дата редактирования')
     slug = models.SlugField(unique=True)
     category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
     collection = models.ForeignKey(Collection, on_delete=models.DO_NOTHING, null=True, verbose_name='Коллекция')

     def save(self, *args, **kwargs):
          self.slug = slugify(self.name)
          super(Product, self).save(*args, **kwargs)

     def __str__(self):
          return self.name


class Order(models.Model):
     created_at = models.DateTimeField(auto_now_add=True)
     modified_at = models.DateTimeField(auto_now=True)
     client_email = models.EmailField()
     client_phone = models.CharField(max_length=20)
     country = models.CharField(max_length=25)
     city = models.CharField(max_length=25)
     total_price = models.DecimalField(max_digits=6, decimal_places=3)


class OrderDetail(models.Model):
     order = models.ForeignKey(Order, on_delete=models.CASCADE)
     product = models.ForeignKey(Product, on_delete=models.CASCADE)
     quantity = models.IntegerField()
     total_price = models.DecimalField(max_digits=6, decimal_places=3)
     created_at = models.DateTimeField(auto_now_add=True)
     modified_at = models.DateTimeField(auto_now=True)
     





