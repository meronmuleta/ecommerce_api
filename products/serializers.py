from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Product, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']
class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()  # Use the nested serializer for category
    class Meta:
        model = Product
        fields = ['id','name','description','price','category','stock_quantity','image_url','created_date']

    #validation to ensure name , price and stock quantity are required
    def validate(self, data):
        if 'name' not in data or not data['name']:
            raise serializers.ValidationError({'name': 'This field is required.'})
        if 'price' not in data or data['price'] is None:
            raise serializers.ValidationError({'price': 'This field is required.'})
        if 'stock_quantity' not in data or data['stock_quantity'] is None:
            raise serializers.ValidationError({'stock_quantity': 'This field is required.'})
        
        #check if price and stock_quantity are positive numbers 
        if data['price'] <= 0:
            raise serializers.ValidationError({'price':'Price must be a positive value.'})
        if data['stock_quantity']< 0:
            raise serializers. ValidationError({'stock_quantity': 'stock quantity cannot be negative.'})
        
        return data
    #method to handle nested category creation
    def create(self, validated_data):
        category_data = validated_data.pop('category')
        category, created = Category.objects.get_or_create(**category_data) #Get or create the category
        product = Product.objects.create(category=category, **validated_data) #Create the product
        return product
    def update(self, instance, validated_data):
        category_data = validated_data.pop('category', None)
        if category_data:
            category, created = Category.objects.get_or_create(**category_data)
            instance.category = category
            
            instance.name = validated_data.get('name', instance.name)
            instance.description = validated_data.get('description', instance.description)
            instance.price = validated_data.get('price', instance.price)
            instance.stock_quantity = validated_data.get('stock_quantity', instance.stock_quantity)
            instance.image_url = validated_data.get('image_url', instance.image_url)
            instance.save()
            return instance

# Get the custom user model
User = get_user_model()
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username','email','password']
        extra_kwargs = {'password':{'write_only':True}} # Password should be write-only

        def create(self, validated_data): 
             # Create a new user with the provided validated data
            user = User.objects.create_user(**validated_data) # This will handle hashing the password
            return user