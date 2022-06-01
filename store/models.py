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
     product = models.ForeignKey("Product", on_delete=models.CASCADE, null=True, related_name='product')

     def __str__(self):
          return f'{self.color}_{self.image}'


class Product(models.Model):

     class Meta:
          verbose_name_plural = 'Товары'
          verbose_name = 'Товар'

     name = models.CharField(max_length=100)
     price = models.IntegerField()
     article = models.CharField(max_length=100, null=True)
     discount_price = models.IntegerField(null=True, blank=True)
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
          if self.discount_percent:
               self.discount_price = self.price - (self.price/100) * self.discount_percent
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


class AboutUsImage(models.Model):
     image = models.ImageField(null=True, blank=True)
     about_us = models.ForeignKey('AboutUs', on_delete=models.CASCADE, null=True)


class AboutUs(models.Model):
     class Meta:
          verbose_name_plural = 'О нас'
          verbose_name = 'О нас'

     title = models.CharField(max_length=100)
     text = RichTextUploadingField('Описание')

     def __str__(self):
          return self.title


class News(models.Model):

     class Meta:
          verbose_name_plural = 'Новости'
          verbose_name = 'Новости'

     title = models.CharField(max_length=100)
     image = models.ImageField()
     text = RichTextUploadingField('Описание')

     def __str__(self):
          return self.title


class Help(models.Model):
     question = models.TextField()
     answer = models.TextField()
     image = models.ForeignKey('HelpImage', on_delete=models.DO_NOTHING, null=True)

     def __str__(self):
          return self.question


class HelpImage(models.Model):
     class Meta:
          verbose_name_plural = 'Вопросы и ответы'
          verbose_name = 'Вопросы и ответы'
     image = models.ImageField()


class PublicOffer(models.Model):

     class Meta:
          verbose_name_plural = 'Публичный оффер'
          verbose_name = 'Публичный оффер'

     title = models.CharField(max_length=100)
     text = RichTextUploadingField('Описание')

     def __str__(self):
          return self.title


class Advantage(models.Model):

     class Meta:
          verbose_name_plural = 'Наши преимущества'
          verbose_name = 'Наши преимущества'

     icon = models.ImageField()
     title = models.CharField(max_length=100)
     text = models.TextField()
     active = models.BooleanField(default=True)

     def __str__(self):
          return self.title


class Slider(models.Model):
     class Meta:
          verbose_name_plural = 'Слайдер '
          verbose_name = 'Слайдер'

     image = models.ImageField()
     link = models.CharField(max_length=150, null=True)
     active = models.BooleanField(default=True)


class CallBack(models.Model):
     class Meta:
          verbose_name_plural = 'Обратный звонок '
          verbose_name = 'Обратный звонок'

     name = models.CharField(max_length=100)
     phone_number = models.CharField(max_length=100)
     date = models.DateField(auto_now_add=True)
     callback_type = models.CharField(max_length=100, null=True)
     contacted = models.BooleanField(default=False)


     def __str__(self):
          if self.contacted:
               return f'Связались'
          return f'Не связались'


class FirstFooter(models.Model):
     class Meta:
          verbose_name_plural = 'Первая вкладка'
          verbose_name = 'Первая вкладка'

     logo = models.ImageField()
     text = models.TextField()
     number = models.CharField(max_length=25)


social_type = (
     ('phone','номер',),
     ('почта', 'mail'),
     ('инстаграм','instagram'),
     ('телеграм','telegram'),
     ('whatsapp','whatsapp')
)


class SecondFooter(models.Model):

     class Meta:
          verbose_name_plural = 'Вторая вкладка'
          verbose_name = 'Вторая вкладка'
     type = models.CharField(choices=social_type, max_length=100)
     link = models.CharField(max_length=100, null=True, verbose_name='ссылка или номер', help_text='номер в формате - 0555555555')

     def save(self, *args, **kwargs):
          if self.type == 'whatsapp':
               # number = re.match(r'^([\s\d]+)$', self.link)
               self.link = f'https://wa.me/{self.link}'
          super(SecondFooter, self).save(*args, **kwargs)


class Favorite(models.Model):
     class Meta:
          abstract = True

     user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)

     def __str__(self):
          return self.user.username


class FavoriteProduct(Favorite):

     obj = models.ForeignKey(Product, verbose_name='продукт', on_delete=models.CASCADE)
