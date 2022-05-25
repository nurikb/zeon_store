from django.db import models
from django.contrib.auth import get_user_model

from colorfield.fields import ColorField
from ckeditor_uploader.fields import RichTextUploadingField
from uuslug import slugify


User = get_user_model()


class Collection(models.Model):
     name = models.CharField(max_length=100)
     image = models.ImageField(default=None)
     slug = models.SlugField(unique=True, null=True, blank=True)

     def save(self, *args, **kwargs):
          self.slug = slugify(self.name)
          super(Collection, self).save(*args, **kwargs)

     def __str__(self):
          return self.name


class Image(models.Model):
     image = models.ImageField(null=True, blank=True)
     color = ColorField()
     product = models.ForeignKey("Product", on_delete=models.CASCADE, null=True)

     def __str__(self):
          return f'{self.color}_{self.image}'


class Product(models.Model):
     name = models.CharField(max_length=100)
     price = models.IntegerField()
     article = models.CharField(max_length=100, null=True)
     discount_price = models.IntegerField(null=True)
     discount_percent = models.IntegerField(null=True)
     slug = models.SlugField(unique=True, null=True, blank=True)
     collection = models.ForeignKey(
          Collection,
          on_delete=models.CASCADE,
          verbose_name='Коллекция',
          related_name='collection',
          null=True
     )
     quantity = models.IntegerField(null=True, verbose_name='количество')
     size = models.CharField(max_length=10, null=True)
     substance = models.CharField(max_length=25, null=True, verbose_name='Состав ткани')
     material = models.CharField(max_length=100, null=True)
     about_text = RichTextUploadingField('Описание товара', null=True, blank=True)
     color = models.CharField(max_length=255, verbose_name='цвет', null=True)
     top_sales = models.BooleanField(default=False)
     new = models.BooleanField(default=True)

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
     order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_detail')
     user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
     product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_product')
     quantity = models.IntegerField()
     total_price = models.DecimalField(max_digits=6, decimal_places=3)
     created_at = models.DateTimeField(auto_now_add=True)
     modified_at = models.DateTimeField(auto_now=True)
     

# class AboutUs(models.Model):
#      text =



