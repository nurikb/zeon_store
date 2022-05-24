from django.db import models
from django.contrib.auth import get_user_model
from ckeditor_uploader.fields import RichTextUploadingField

from uuslug import slugify


User = get_user_model()


class Collection(models.Model):
     name = models.CharField(max_length=100)
     slug = models.SlugField(unique=True, null=True, blank=True)

     def save(self, *args, **kwargs):
          self.slug = slugify(self.name)
          super(Collection, self).save(*args, **kwargs)

     def __str__(self):
          return self.name


class Product(models.Model):
     name = models.CharField(max_length=100)
     price = models.DecimalField(max_digits=6, decimal_places=0)
     created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
     modified_at = models.DateTimeField(auto_now=True, verbose_name='Дата редактирования')
     slug = models.SlugField(unique=True)
     collection = models.ManyToManyField(
          to=Collection,
          verbose_name='Коллекция',
          related_name='collection'
     )
     quantity = models.IntegerField(null=True)
     size = models.CharField(max_length=10, null=True)
     substance = models.CharField(max_length=25, null=True)
     about_text = RichTextUploadingField('Описание товара', null=True, blank=True)

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



