import re

from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models


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


class PublicOffer(models.Model):

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
               self.link = 'https://wa.me/'+''.join(re.findall(r'\d' ,self.link))
          super(SecondFooter, self).save(*args, **kwargs)
