import requests
import random
import string
import allure
from config import Endpoints


def generate_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


@allure.step("Создание заказа")
def create_order(color=None):
    payload = {
        "firstName": "Naruto",
        "lastName": "Uchiha",
        "address": "Konoha, 142 apt.",
        "metroStation": 4,
        "phone": "+7 800 355 35 35",
        "rentTime": 5,
        "deliveryDate": "2020-06-06",
        "comment": "Saske, come back to Konoha"
    }
    
    if color:
        payload["color"] = color
        
    url = Endpoints.get_full_url(Endpoints.ORDERS)
    return requests.post(url, json=payload)