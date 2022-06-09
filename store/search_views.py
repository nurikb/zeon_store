import random

from rest_framework import generics
from rest_framework.filters import SearchFilter

from cart.favorite import Favorite
from store.models import Product
from store.serializers import SearhcWithHintSerializer, SimilarProductSerializer


class SearchAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = SimilarProductSerializer
    filter_backends = [SearchFilter]
    search_fields = ('name', 'collection__name')

    def list(self, request, *args, **kwargs):

        """
        переопределил list(): если нет результата функции self.filter_queryset()
        добавил 5 обьектов класса(модели) Product
        """

        queryset = self.get_queryset()
        filtered_queryset = self.filter_queryset(queryset)
        filtered_queryset_status = True
        hints = SearhcWithHintSerializer(filtered_queryset, many=True).data

        if not filtered_queryset:
            filtered_queryset_status = False
            collection_id_list = list(set(queryset.values_list('collection_id')))[:5]

            product_id_list = [random.choice(queryset.filter(collection_id=c_product)).id for c_product in
                               collection_id_list]
            filtered_queryset = queryset.filter(id__in=product_id_list)

        page = self.paginate_queryset(filtered_queryset)
        favorite = Favorite(request)
        search_param = self.request.GET.get('search')

        serializer = self.get_serializer(page, many=True, context={'favorite': favorite.favorite})
        return self.get_paginated_response({'search_result': serializer.data, 'hints': hints,
                                            'search_param': search_param, 'search_status': filtered_queryset_status})
