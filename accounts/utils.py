import random

from django.contrib.auth import get_user_model

User = get_user_model()


def generate_username(first_name):
    while True:
        random_number = random.randint(100, 999)
        username = f"{first_name.lower()}_{random_number}"

        if not User.objects.filter(username=username).exists():
            return username


def generate_password(first_name, phone_number):
    password = f"{first_name.lower()}@{phone_number}"
    return password
