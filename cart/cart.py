from decimal import Decimal
from django.conf import settings
from store.models import Product


class Cart(object):
    def __init__(self, request):
        # Инициализация корзины пользователя
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # Сохраняем корзину пользователя в сессию
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    # Добавление товар в корзину пользователя
    # или обновление количества товаров
    def add(self, product, quantity=1, update_quantity=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                     'price': str(product.price),
                                     'discount_price': str(product.discount_price)}
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

        # Сохранение данных в сессию
    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        # Указываем, что сессия изменена
        self.session.modified = True

        # Удаление товара из корзины
    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()


    # Итерация по товарам
    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            item['test'] = 3333
            yield item

    # Количество товаро
    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        price = sum(Decimal(item['price'])*item['quantity'] for item in self.cart.values())
        discount_price = sum(Decimal(item['discount_price'])*item['quantity'] for item in self.cart.values())
        return {'price': price, 'discount_price': discount_price}

    def get_full_cart(self):
        product_ids = self.cart.keys()
        product_list = Product.objects.filter(id__in=product_ids)
        return product_list

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
