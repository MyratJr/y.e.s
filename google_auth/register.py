from users.models import User
import os
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import authenticate
import random
from string import ascii_lowercase


def generate_username(user_id):
    alphabet = ascii_lowercase
    random_letters = random.sample(alphabet, 5)
    return ''.join(random_letters)+str(user_id)


def register_social_user(provider, user_id, email):
    filtered_user_by_email = User.objects.filter(email=email)
    
    if filtered_user_by_email.exists():
        if provider == filtered_user_by_email[0].registration_method:
            authenticate(email=email, password=os.environ.get('SOCIAL_AUTH_PASSWORD'))
            return {
                "username": filtered_user_by_email[0].username,
                "email": filtered_user_by_email[0].email, 
                "tokens": filtered_user_by_email[0].tokens()  
            }
        else:
            raise AuthenticationFailed(
                detail="Please continue your login using" + filtered_user_by_email[0].registration_method
            )
        
    else:
        user = {
            'username': generate_username(user_id), 'email': email,
            'password': os.environ.get('SOCIAL_AUTH_PASSWORD')}
        user = User.objects.create_user(**user)
        user.registration_method = provider
        user.save()

        authenticate(
            email=email, password=os.environ.get('SOCIAL_AUTH_PASSWORD'))
        return {
            'email': user.email,
            'username': user.username,
            'tokens': user.tokens()
        }