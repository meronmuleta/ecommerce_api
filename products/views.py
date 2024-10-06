from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Product
from django.contrib.auth.models import User
from .serializers import ProductSerializer, UserSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('id')  # Add ordering here
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly] # Authenticated users can manage products


     # Custom search endpoint
    @action(detail=False,methods=['get'])
    def search(self,request):
        name_query = request.query_params.get('name', '')
        category_query = request.query_params.get('category','')

        # Filtering by name and category
        queryset = self.get_queryset().filter(name__icontains=name_query, category__name__icontains=category_query)

         # Handle pagination
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many= True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
     # Custom filter endpoint with additional query parameters
    @action(detail=False, methods=['get'],url_path='filter')
    def filter(self,request):
        category = request.query_params.get('category', None)
        price_min = request.query_params.get('price_min', None)
        price_max = request.query_params.get('price_max', None)
        stock_min = request.query_params.get('stock_min', None)
 
        # Start with all products
        queryset = self.get_queryset()
        # Apply filtering based on query parameters
        if category:
            queryset = queryset.filter(category__name=category)
        if price_min:
            queryset = queryset.filter(price__gte=price_min)
        if price_max:
            queryset = queryset.filter(price__lte=price_max)
        if stock_min:
            queryset = queryset.filter(stock_quantity__gte=stock_min)

        # Handle pagination
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
  
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


    def get_permissions(self):
        # Allow only superusers to create, update, or delete users
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            self.permission_classes = [IsAdminUser]  # Only superusers can manage users
        else:
            self.permission_classes = [IsAuthenticated]  # Authenticated users can view their own data
        return super().get_permissions()

    def get_queryset(self):
        # If user is not a superuser, limit queryset to the requesting user
        if not self.request.user.is_superuser:
            return self.queryset.filter(id=self.request.user.id)
        return self.queryset  # Superuser can see all users



 

