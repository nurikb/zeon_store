from zeon_store.settings import FAVORITE_SESSION_ID
from store.models import Product


class Favorite(object):
    def __init__(self, request):
        self.session = request.session
        favorite = self.session.get(FAVORITE_SESSION_ID)
        if not favorite:
            favorite = self.session[FAVORITE_SESSION_ID] = []
        self.favorite = favorite

    def add(self, product):
        product_id = product.id
        if product_id not in self.favorite:
            self.favorite.append(product_id)
        self.save()

    def save(self):
        self.session[FAVORITE_SESSION_ID] = self.favorite
        self.session.modified = True

    def remove(self, product):
        product_id = product.id
        if product_id in self.favorite:
            self.favorite.remove(product_id)
            self.save()

    def get_favorite(self):
        product_ids = self.favorite
        product_list = Product.objects.filter(id__in=product_ids)
        return product_list

    def clear(self):
        del self.session[FAVORITE_SESSION_ID]
        self.session.modified = True