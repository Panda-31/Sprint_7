# test_data.py
from helpers.courier_helpers import generate_random_string


class TestData:
    
    @staticmethod
    def get_courier_data():
        return {
            "login": generate_random_string(10),
            "password": generate_random_string(10),
            "firstName": generate_random_string(10)
        }
    
    @staticmethod
    def get_courier_data_without_firstname():
        return {
            "login": generate_random_string(10),
            "password": generate_random_string(10)
        }
    
    @staticmethod
    def get_order_data():
        return {
            "firstName": "Test",
            "lastName": "User",
            "address": "Test address, 123",
            "metroStation": 4,
            "phone": "+7 800 355 35 35",
            "rentTime": 3,
            "deliveryDate": "2024-12-31",
            "comment": "Test order"
        }
    
    BLACK_ONLY = ["BLACK"]
    GREY_ONLY = ["GREY"]
    BOTH_COLORS = ["BLACK", "GREY"]