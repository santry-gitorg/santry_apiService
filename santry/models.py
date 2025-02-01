from django.db import models
from datetime import datetime, timedelta

def get_default_expiry_date():
    return datetime.now() + timedelta(days=30)

def get_default_user():
    try:
        return User.objects.first()
    except User.DoesNotExist:
        return None

class User(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=100, default='New User', null=True)
    age = models.IntegerField(null=True)
    weight = models.FloatField(null=True)
    profile_picture_url = models.TextField(null=True)
    dietary_preferences = models.TextField(null=True)
    santry_green_score = models.IntegerField(null=True)

class FoodItem(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, default='sample food item')
    barcode = models.CharField(max_length=50, null=True)
    image = models.TextField(null=True)
    category = models.CharField(max_length=50, default='Uncategorized', null=True)
    quantity = models.FloatField(null=True)
    unit = models.CharField(max_length=20, default='pieces')
    expiry_date = models.DateField(default=get_default_expiry_date)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=get_default_user)

class FoodItemTag(models.Model):
    id = models.AutoField(primary_key=True)
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE, related_name='tags')
    tag = models.CharField(max_length=100, default='sample tag')

class Recipe(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, default='sample recipe')
    description = models.TextField(null=True)
    image = models.TextField(null=True)
    instructions = models.TextField(null=True)
    dietary_restrictions = models.TextField(null=True)

class RecipeIngredient(models.Model):
    id = models.AutoField(primary_key=True)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='recipe_ingredients')
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.FloatField(null=True)
    unit = models.CharField(max_length=20, default='', null=True)

class RecipeSuggestion(models.Model):
    id = models.AutoField(primary_key=True)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='suggestions')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipe_suggestions')
    suggested_on = models.DateTimeField(auto_now_add=True)

class Notification(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField(null=True)
    triggered_on = models.DateTimeField(auto_now_add=True, null=True)