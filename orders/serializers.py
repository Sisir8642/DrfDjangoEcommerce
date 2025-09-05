from rest_framework import serializers
from .models import Order, OrderItem
from products.models import Product
from users.models import User

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'quantity', 'price_at_order']
        read_only_fields = ['price_at_order']

class OrderStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status']

class UserValidationSerializer(serializers.ModelSerializer):
    class Meta:
        model= User
        fields = ['id', 'username', 'email', 'role'] 

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True,)
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        user = obj.user
        return {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role,
        }


    class Meta:
        model = Order
        fields = ['id', 'user', 'status', 'created_at', 'updated_at', 'items']
        read_only_fields = ['user','status', 'created_at', 'updated_at']
        

    def validate_items(self, value):
        if not value:
            raise serializers.ValidationError("Order must contain at least one item.")
        for item in value:
            if item.get('quantity', 0) <= 0:
                raise serializers.ValidationError("Select product")
        return value

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        user = self.context['request'].user
        validated_data.pop('user', None)

        order = Order.objects.create(user=user, **validated_data)

        for item_data in items_data:
            product = item_data['product']
            quantity = item_data['quantity']
            product_name = item_data['product'].name
            OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity,
            
            price_at_order=product.price
        )

        return order


    def update(self, instance, validated_data):
        items_data = validated_data.pop('items', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if items_data is not None:
            instance.items.all().delete()

            for item_data in items_data:
                OrderItem.objects.create(
                order=instance,
                product=item_data['product'],
                quantity=item_data['quantity'],
                product_name = item_data['product'].name,
                price_at_order=item_data['product'].price
            )

        return instance
    

