import requests
import allure
from config import Endpoints
import random
import string


def generate_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


def create_order_black():
    payload = {
        "firstName": "Naruto",
        "lastName": "Uchiha",
        "address": "Konoha, 142 apt.",
        "metroStation": 4,
        "phone": "+7 800 355 35 35",
        "rentTime": 5,
        "deliveryDate": "2020-06-06",
        "comment": "Saske, come back to Konoha",
        "color": ["BLACK"]
    }
    
    url = Endpoints.get_full_url(Endpoints.ORDERS)
    return requests.post(url, json=payload)


def create_order_grey():
    payload = {
        "firstName": "Naruto",
        "lastName": "Uchiha",
        "address": "Konoha, 142 apt.",
        "metroStation": 4,
        "phone": "+7 800 355 35 35",
        "rentTime": 5,
        "deliveryDate": "2020-06-06",
        "comment": "Saske, come back to Konoha",
        "color": ["GREY"]
    }
    
    url = Endpoints.get_full_url(Endpoints.ORDERS)
    return requests.post(url, json=payload)


def create_order_both_colors():
    payload = {
        "firstName": "Naruto",
        "lastName": "Uchiha",
        "address": "Konoha, 142 apt.",
        "metroStation": 4,
        "phone": "+7 800 355 35 35",
        "rentTime": 5,
        "deliveryDate": "2020-06-06",
        "comment": "Saske, come back to Konoha",
        "color": ["BLACK", "GREY"]
    }
    
    url = Endpoints.get_full_url(Endpoints.ORDERS)
    return requests.post(url, json=payload)


def create_order_without_color():
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
    
    url = Endpoints.get_full_url(Endpoints.ORDERS)
    return requests.post(url, json=payload)


def register_courier(login, password, first_name=None):
    payload = {"login": login, "password": password}
    if first_name:
        payload["firstName"] = first_name
    
    url = Endpoints.get_full_url(Endpoints.COURIER)
    return requests.post(url, data=payload)