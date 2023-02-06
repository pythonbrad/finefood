from core.models import (
    Menu, Feedback, Category, Book,
    Restaurant, User
)
import random
import json

def create_user(data):
    user = User.objects.get_or_create(
        username=data['username'],
        defaults={
            'email': data['email'],
            'first_name': data['first_name'],
            'last_name': data['last_name'],
            'address': data['address'],
            'phone_number': data['phone_number'],
        },
    )[0]
    user.set_password(data['password'])
    user.save()
    return user

def exec():
    # We create the users
    with open('dummy_data.json') as f:
        data = json.load(f)
    
    for d in data:
        user = create_user(d)

        for rd in d['restaurants']:
            restaurant = Restaurant.objects.get_or_create(
                name=rd['name'],
                defaults={
                    'has_delivery': rd['has_delivery'],
                    'description': rd['description'],
                    'address': rd['address'],
                    'working_days': rd['working_days'],
                    'working_hours': rd['working_hours'],
                    'base_currency': rd['base_currency'],
                    'gmt': rd['gmt'],
                }
            )[0]
            restaurant.managers.add(user)
            menu = Menu.objects.get_or_create(
                name=rd['menu']['name'],
                entry_ref=restaurant,
                defaults={
                    'description': rd['menu']['description'],

                }
            )[0]

            for _ in rd['menu']['items']:
                menu.items.get_or_create(
                    name=_['name'],
                    category=Category.objects.get_or_create(
                        name=_['category'],
                        entry_ref=restaurant,
                    )[0],
                    defaults={
                        'price': _['price'],
                    }
                )[0]

            for _ in rd['waiters']:
                restaurant.waiters.add(create_user(_))

            for _ in rd['managers']:
                restaurant.managers.add(create_user(_))

            for _ in rd['chefs']:
                restaurant.waiters.add(create_user(_))

            for _ in rd['feedbacks']:
                Feedback.objects.create(
                    customer=create_user(_['customer']),
                    content=_['content'],
                    entry_ref=restaurant
                )

    # We book a restaurant
    for user in User.objects.filter():
        book = Book.objects.get_or_create(
            customer=user,
        )[0]
        [
            book.restaurants.add(restaurant)
            for restaurant in Restaurant.objects.filter().order_by('?')
            if random.choice([0, 1, 0])
        ]
