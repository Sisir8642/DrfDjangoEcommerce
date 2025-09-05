from django.shortcuts import render
from rest_framework import viewsets
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
from .permissions import IsAdmin, IsCustomer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny


# Create your views here.
class CategoryViewSet(viewsets.ModelViewSet):
    queryset= Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdmin]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class= ProductSerializer
    permission_classes=[IsAuthenticated]

    
    @action(detail=True, methods =['patch'], permission_classes=[IsAdmin])
    def toggle(self, request, pk=None):
        product = self.get_object()
        product.is_active = not product.is_active
        product.save()
        return Response({
        'status': 'updated',
        'product_id': product.id,
        'is_active': product.is_active
        })

class ActiveViewSet(viewsets.ReadOnlyModelViewSet):
    queryset= Product.objects.filter(is_active = True)
    serializer_class= ProductSerializer
    permission_classes = [ AllowAny]
