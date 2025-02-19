from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'age', 'weight', 'profile_picture_url', 'created_at']
        read_only_fields = ['id', 'created_at']

class DietaryPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DietaryPreference
        fields = ['id', 'preference_name']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'category_name', 'approx_expiry_time']

class FoodItemSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    
    class Meta:
        model = FoodItem
        fields = ['id', 'name', 'picture_url', 'quantity', 'quantity_unit', 
                 'expiry_date', 'input_method', 'categories', 'created_at']
        read_only_fields = ['id', 'created_at']

class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ['id', 'title', 'description', 'instructions', 
                 'dish_photo', 'created_at']
        read_only_fields = ['id', 'created_at']

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'type', 'message', 'is_read', 'created_at']
        read_only_fields = ['id', 'created_at']