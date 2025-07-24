# common/confirmation.py
import random
from django.core.cache import cache

CONFIRMATION_CODE_TTL = 300  # 5 минут

def generate_confirmation_code():
    return f"{random.randint(100000, 999999)}"

def save_confirmation_code(email, code=None):
    if not code:
        code = generate_confirmation_code()
    key = f"user_confirmation_code_{email}"

    # удалить старый, если есть
    cache.delete(key)

    # сохранить с TTL 5 минут
    cache.set(key, code, timeout=CONFIRMATION_CODE_TTL)
    return code

def get_confirmation_code(email):
    key = f"user_confirmation_code_{email}"
    return cache.get(key)

def delete_confirmation_code(email):
    key = f"user_confirmation_code_{email}"
    cache.delete(key)
