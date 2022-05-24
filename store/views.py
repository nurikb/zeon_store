from rest_framework import viewsets
from rest_framework import permissions
from store.models import Product, Collection
from store.serializers import ProductSerializer, CollectionSerializer


class ProductViewSet(viewsets.ModelViewSet):
    """
    API
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CollectionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
