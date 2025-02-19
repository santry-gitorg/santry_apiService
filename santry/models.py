from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class User(AbstractUser):
    id = models.CharField(max_length=36, primary_key=True)  # This will store the Firebase UID
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    age = models.IntegerField(null=True, blank=True)
    weight = models.IntegerField(null=True, blank=True)
    profile_picture_url = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    class Meta:
        db_table = 'users'

    def __str__(self):
        return '{}'.format(self.name) + ' - ' + '{}'.format(self.id)

class DietaryPreference(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    preference_name = models.CharField(max_length=100)

    class Meta:
        db_table = 'dietary_preferences'
    
    def __str__(self):
        return '{}'.format(self.preference_name)

class UserDietaryPreference(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dietary_preferences')
    preference = models.ForeignKey(DietaryPreference, on_delete=models.CASCADE)

    class Meta:
        db_table = 'user_dietary_preferences'
        unique_together = ('user', 'preference')

class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category_name = models.CharField(max_length=100)
    approx_expiry_time = models.IntegerField(help_text='in days')

    class Meta:
        db_table = 'category'
        verbose_name_plural = 'categories'
    
    def __str__(self):
        return '{}'.format(self.category_name)

class FoodItem(models.Model):
    class QuantityUnit(models.TextChoices):
        KILOGRAM = 'KG', 'Kilogram'
        UNIT = 'UNIT', 'Unit'
        GRAM = 'G', 'Gram'

    class InputMethod(models.TextChoices):
        BARCODE = 'BAR', 'Barcode'
        IMAGE = 'IMG', 'Image'
        MANUAL = 'MAN', 'Manual'
        SCAN = 'SCA', 'Scan'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='food_items')
    name = models.CharField(max_length=100)
    picture_url = models.CharField(max_length=255, null=True, blank=True)
    quantity = models.IntegerField()
    quantity_unit = models.CharField(max_length=4, choices=QuantityUnit.choices)
    expiry_date = models.DateTimeField()
    input_method = models.CharField(max_length=3, choices=InputMethod.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField(Category, through='FoodItemCategory')

    class Meta:
        db_table = 'food_items'

    def __str__(self):
        return '{}'.format(self.name)

class FoodItemCategory(models.Model):
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        db_table = 'food_item_category'
        unique_together = ('food_item', 'category')

class Recipe(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes')
    title = models.CharField(max_length=100)
    description = models.TextField()
    instructions = models.TextField()
    dish_photo = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'recipes'

    def __str__(self):
        return '{}'.format(self.title)

class Notification(models.Model):
    class NotificationType(models.TextChoices):
        EXPIRY = 'EXP', 'Expiry'
        RECIPE = 'REC', 'Recipe'
        SYSTEM = 'SYS', 'System'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    type = models.CharField(max_length=3, choices=NotificationType.choices)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'notifications'
    
    def __str__(self):
        return '{}'.format(self.message)