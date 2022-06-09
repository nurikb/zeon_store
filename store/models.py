import re
from django.db import models
from django.contrib.auth import get_user_model

from colorfield.fields import ColorField
from ckeditor_uploader.fields import RichTextUploadingField
from uuslug import slugify


User = get_user_model()


class Collection(models.Model):

     class Meta:
          verbose_name_plural = 'Коллекция'
          verbose_name = 'Коллекция'

     name = models.CharField(max_length=100, verbose_name='название')
     image = models.ImageField(default=None, verbose_name='картинка')
     slug = models.SlugField(unique=True, null=True, blank=True)

     def save(self, *args, **kwargs):
          self.slug = slugify(self.name)
          super(Collection, self).save(*args, **kwargs)

     def __str__(self):
          return self.name


class Image(models.Model):
     image = models.ImageField(null=True, blank=True, verbose_name='картина под цвет продукта')
     color = ColorField(verbose_name='цвет продукта')
     product = models.ForeignKey("Product", on_delete=models.CASCADE, null=True, related_name='product_image')


class Product(models.Model):

     class Meta:
          verbose_name_plural = 'Товары'
          verbose_name = 'Товар'

     name = models.CharField(max_length=100, verbose_name='название')
     price = models.IntegerField(verbose_name='цена')
     article = models.CharField(max_length=100, null=True, verbose_name='артикул')
     discount_price = models.IntegerField(null=True, blank=True, verbose_name='цена со скидкой')
     discount_percent = models.IntegerField(null=True, blank=True, verbose_name='скидка')
     slug = models.SlugField(unique=True, null=True, blank=True)
     collection = models.ForeignKey(
          Collection,
          on_delete=models.CASCADE,
          verbose_name='Коллекция',
          related_name='collection',
          null=True
     )
     quantity = models.IntegerField(null=True, verbose_name='количество')
     size = models.CharField(max_length=10, null=True, verbose_name='размер', help_text="писать в формате: 40-60")
     substance = models.CharField(max_length=25, null=True, verbose_name='Состав ткани')
     material = models.CharField(max_length=100, null=True, verbose_name='материал')
     about_text = RichTextUploadingField('Описание товара', null=True, blank=True)
     top_sales = models.BooleanField(default=False, verbose_name='хит продаж')
     new = models.BooleanField(default=True, verbose_name='новинки')

     def save(self, *args, **kwargs):
          # self.slug = slugify(self.name)
          if self.discount_percent:
               self.discount_price = self.price - (self.price/100) * self.discount_percent
          else:
               self.discount_price = None
               self.discount_percent = 0

          size_list = self.size.split('-')
          if len(size_list) == 2:
               self.quantity = ((int(size_list[1]) - int(size_list[0])) / 2)+1
          super(Product, self).save(*args, **kwargs)

     def __str__(self):
          return self.name


class Order(models.Model):
     class Meta:
          verbose_name_plural = 'Заказы'
          verbose_name = 'Заказы'

     product_quantity = models.IntegerField(null=True, verbose_name='количество линеек')
     total_quantity = models.IntegerField(null=True, verbose_name='количество товаров')
     discount_sum = models.IntegerField(null=True, verbose_name='скидка')
     discount_price = models.IntegerField(null=True, verbose_name='итого к оплате')
     total_price = models.IntegerField(null=True, verbose_name='стоимость')

     def __str__(self):
          print(self.order_client)
          return 'dfasdf'


class OrderDetail(models.Model):
     product_image = models.ForeignKey(Image, on_delete=models.CASCADE, null=True, verbose_name='картина/цвет товара')
     order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_detail', verbose_name='заказ')
     product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_product', verbose_name='товар')
     quantity = models.IntegerField(null=True, verbose_name='количество заказанных товаров')
     color = ColorField(null=True)

     def save(self, *args, **kwargs):
          self.color = self.product_image.color
          super(OrderDetail, self).save(*args, **kwargs)


status_choice = (
     ('Новый', 'Новый',),
     ('Оформлен', 'Оформлен'),
     ('Отменен', 'Отменен'),
)


class Client(models.Model):
     class Meta:
          verbose_name_plural = 'Клиенты'
          verbose_name = 'Клиенты'

     name = models.CharField(max_length=100, verbose_name='имя')
     surname = models.CharField(max_length=100, verbose_name='фамилия')
     country = models.CharField(max_length=100, verbose_name='страна')
     city = models.CharField(max_length=100, verbose_name='город')
     email = models.EmailField(verbose_name='эл. почта')
     order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, related_name='order_client')
     date = models.DateField(auto_now_add=True, verbose_name='дата оформления')
     status = models.CharField(choices=status_choice, max_length=20, default='Новый', verbose_name='статус')

     def __str__(self):
          return f'{self.status}-{self.name}'


class Favorite(models.Model):
     class Meta:
          abstract = True

     user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)

     def __str__(self):
          return self.user.username


class FavoriteProduct(Favorite):

     obj = models.ForeignKey(Product, verbose_name='продукт', on_delete=models.CASCADE)
