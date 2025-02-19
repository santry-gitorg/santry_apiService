import os
import django
import sys

# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'santry_APIservice.settings')  # Replace 'your_project' with your actual project name
django.setup()

from django.utils import timezone
from datetime import timedelta
import random
from santry.models import *

def run():
    # Clear existing data
    print("Clearing existing data...")
    User.objects.all().delete()
    DietaryPreference.objects.all().delete()
    Category.objects.all().delete()
    Recipe.objects.all().delete()
    Notification.objects.all().delete()

    print("Creating new test data...")
    
    # 1. Create Users
    users_data = [
        {
            'id': 'firebase1111111111111111111',
            'username': 'john_doe',
            'name': 'John Doe',
            'email': 'john@example.com',
            'age': 28,
            'weight': 75,
        },
        {
            'id': 'firebase2222222222222222222',
            'username': 'jane_smith',
            'name': 'Jane Smith',
            'email': 'jane@example.com',
            'age': 32,
            'weight': 65,
        },
        {
            'id': 'firebase3333333333333333333',
            'username': 'mike_wilson',
            'name': 'Mike Wilson',
            'email': 'mike@example.com',
            'age': 45,
            'weight': 80,
        }
    ]

    for user_data in users_data:
        User.objects.create_user(
            id=user_data['id'],
            username=user_data['username'],
            name=user_data['name'],
            email=user_data['email'],
            age=user_data['age'],
            weight=user_data['weight'],
            password='testpass123'
        )
    print("Created users")

    # 2. Create Dietary Preferences
    preferences_data = [
        'Vegetarian',
        'Vegan',
        'Gluten-free',
        'Lactose-free',
        'Keto'
    ]

    dietary_prefs = []
    for pref_name in preferences_data:
        pref = DietaryPreference.objects.create(preference_name=pref_name)
        dietary_prefs.append(pref)
    print("Created dietary preferences")

    # 3. Assign Dietary Preferences to Users
    for user in User.objects.all():
        selected_prefs = random.sample(dietary_prefs, 2)
        for pref in selected_prefs:
            UserDietaryPreference.objects.create(user=user, preference=pref)
    print("Assigned dietary preferences to users")

    # 4. Create Categories
    categories_data = [
        ('Fruits', 7),
        ('Vegetables', 5),
        ('Dairy', 14),
        ('Meat', 3),
        ('Grains', 90)
    ]

    categories = []
    for cat_name, expiry in categories_data:
        category = Category.objects.create(
            category_name=cat_name,
            approx_expiry_time=expiry
        )
        categories.append(category)
    print("Created categories")

    # 5. Create Food Items
    foods_data = [
        {
            'name': 'Apples',
            'quantity': 6,
            'quantity_unit': 'UNIT',
            'input_method': 'MAN',
            'categories': ['Fruits']
        },
        {
            'name': 'Milk',
            'quantity': 1,
            'quantity_unit': 'UNIT',
            'input_method': 'BAR',
            'categories': ['Dairy']
        },
        {
            'name': 'Chicken',
            'quantity': 500,
            'quantity_unit': 'G',
            'input_method': 'MAN',
            'categories': ['Meat']
        },
        {
            'name': 'Rice',
            'quantity': 1,
            'quantity_unit': 'KG',
            'input_method': 'MAN',
            'categories': ['Grains']
        }
    ]

    for user in User.objects.all():
        for food in foods_data:
            food_item = FoodItem.objects.create(
                user=user,
                name=food['name'],
                quantity=food['quantity'],
                quantity_unit=food['quantity_unit'],
                expiry_date=timezone.now() + timedelta(days=random.randint(1, 30)),
                input_method=food['input_method']
            )
            for cat_name in food['categories']:
                category = Category.objects.get(category_name=cat_name)
                food_item.categories.add(category)
    print("Created food items")

    # 6. Create Recipes
    recipes_data = [
        {
            'title': 'Chicken Curry',
            'description': 'A delicious Indian curry',
            'instructions': '1. Cook chicken\n2. Add spices\n3. Simmer'
        },
        {
            'title': 'Apple Pie',
            'description': 'Classic dessert',
            'instructions': '1. Make dough\n2. Prepare filling\n3. Bake'
        },
        {
            'title': 'Vegetable Stir Fry',
            'description': 'Quick and healthy',
            'instructions': '1. Chop vegetables\n2. Heat oil\n3. Stir fry'
        }
    ]

    for user in User.objects.all():
        for recipe in recipes_data:
            Recipe.objects.create(
                user=user,
                **recipe
            )
    print("Created recipes")

    # 7. Create Notifications
    notifications_data = [
        {
            'type': 'EXP',
            'message': 'Your milk is expiring soon!'
        },
        {
            'type': 'REC',
            'message': 'New recipe suggestion: Try making apple pie!'
        },
        {
            'type': 'SYS',
            'message': 'Welcome to Santry!'
        }
    ]

    for user in User.objects.all():
        for notif in notifications_data:
            Notification.objects.create(
                user=user,
                **notif
            )
    print("Created notifications")

    # Print summary
    print("\nSummary of created data:")
    print(f"Users: {User.objects.count()}")
    print(f"DietaryPreferences: {DietaryPreference.objects.count()}")
    print(f"Categories: {Category.objects.count()}")
    print(f"FoodItems: {FoodItem.objects.count()}")
    print(f"Recipes: {Recipe.objects.count()}")
    print(f"Notifications: {Notification.objects.count()}")

if __name__ == '__main__':
    run()