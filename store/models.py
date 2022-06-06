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
     discount_percent = models.IntegerField(null=True, verbose_name='скидка')
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

          size_list = self.size.split('-')
          if len(size_list) == 2:
               self.quantity = ((int(size_list[1]) - int(size_list[0])) / 2)+1
          super(Product, self).save(*args, **kwargs)

     def __str__(self):
          return self.name


class Order(models.Model):
     product_quantity = models.IntegerField(null=True, verbose_name='количество линеек')
     total_quantity = models.IntegerField(null=True, verbose_name='количество товаров')
     discount_sum = models.IntegerField(null=True, verbose_name='скидка')
     discount_price = models.IntegerField(null=True, verbose_name='итого к оплате')
     total_price = models.IntegerField(null=True, verbose_name='стоимость')


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
     order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
     date = models.DateField(auto_now_add=True, verbose_name='дата оформления')
     status = models.CharField(choices=status_choice, max_length=20, default='Новый', verbose_name='статус')

     def __str__(self):
          return f'{self.status}-{self.name}'


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

     title = models.CharField(max_length=100, verbose_name='заголовок')
     image = models.ImageField(verbose_name='картинка')
     text = RichTextUploadingField('Описание')

     def __str__(self):
          return self.title


class Help(models.Model):
     question = models.TextField(verbose_name='вопрос')
     answer = models.TextField(verbose_name='ответ')
     image = models.ForeignKey('HelpImage', on_delete=models.DO_NOTHING, null=True)

     def __str__(self):
          return self.question


class HelpImage(models.Model):
     class Meta:
          verbose_name_plural = 'Вопросы и ответы'
          verbose_name = 'Вопросы и ответы'
     image = models.ImageField(verbose_name='картина')


class     PublicOffer(models.Model):

     class Meta:
          verbose_name_plural = 'Публичный оффер'
          verbose_name = 'Публичный оффер'

     title = models.CharField(max_length=100, verbose_name='заголовок')
     text = RichTextUploadingField('Описание')

     def __str__(self):
          return self.title


class Advantage(models.Model):

     class Meta:
          verbose_name_plural = 'Наши преимущества'
          verbose_name = 'Наши преимущества'

     icon = models.ImageField(verbose_name='иконка')
     title = models.CharField(max_length=100, verbose_name='заголовок')
     text = models.TextField(verbose_name='описание')
     active = models.BooleanField(default=True, verbose_name='показывать на сайте?')

     def __str__(self):
          return self.title


class Slider(models.Model):
     class Meta:
          verbose_name_plural = 'Слайдер '
          verbose_name = 'Слайдер'

     image = models.ImageField(verbose_name='картинка')
     link = models.CharField(max_length=150, null=True, verbose_name='ссылка')
     active = models.BooleanField(default=True, verbose_name='показывать на сайте?')


class CallBack(models.Model):
     class Meta:
          verbose_name_plural = 'Обратный звонок '
          verbose_name = 'Обратный звонок'

     name = models.CharField(max_length=100, verbose_name='имя')
     phone_number = models.CharField(max_length=100, verbose_name='номер')
     date = models.DateField(auto_now_add=True)
     callback_type = models.CharField(max_length=100, null=True, verbose_name='тип обращения')
     contacted = models.BooleanField(default=False, verbose_name='статус')

     def __str__(self):
          if self.contacted:
               return f'Связались'
          return f'Не связались'


class FirstFooter(models.Model):
     class Meta:
          verbose_name_plural = 'Футер'
          verbose_name = 'Футер'

     logo = models.ImageField(verbose_name='логотип')
     text = models.TextField(verbose_name='текстовая информация')
     number = models.CharField(max_length=25, verbose_name='номер в хедере')


social_type = (
     ('phone','номер',),
     ('почта', 'mail'),
     ('инстаграм','instagram'),
     ('телеграм','telegram'),
     ('whatsapp','whatsapp')
)


class SecondFooter(models.Model):

     class Meta:
          verbose_name_plural = 'Номера телефонов'
          verbose_name = 'Номера телефонов'
     type = models.CharField(choices=social_type, max_length=100, verbose_name='тип')
     link = models.CharField(max_length=100, null=True, verbose_name='ссылка или номер', help_text='номер в формате - 0555555555')
     footer = models.ForeignKey(FirstFooter, on_delete=models.CASCADE, null=True)

     def save(self, *args, **kwargs):
          if self.type == 'whatsapp':
               self.link = 'https://wa.me/'+''.join(re.findall(r'\d' ,self.type))
          super(SecondFooter, self).save(*args, **kwargs)


class Favorite(models.Model):
     class Meta:
          abstract = True

     user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)

     def __str__(self):
          return self.user.username


class FavoriteProduct(Favorite):

     obj = models.ForeignKey(Product, verbose_name='продукт', on_delete=models.CASCADE)
