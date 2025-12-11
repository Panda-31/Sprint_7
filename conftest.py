import pytest
import requests
import allure
from helpers.courier_helpers import (
    register_new_courier_and_return_login_password,
    delete_courier,
    login_courier
)


@pytest.fixture
def create_and_delete_courier():
    courier_data = register_new_courier_and_return_login_password()
    if len(courier_data) == 0:
        import random
        import string
        letters = string.ascii_lowercase
        login = ''.join(random.choice(letters) for i in range(10))
        password = ''.join(random.choice(letters) for i in range(10))
        
        payload = {"login": login, "password": password}
        response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier', data=payload)
        
        if response.status_code == 201:
            courier_data = [login, password, ""]
    
    if len(courier_data) == 3:
        login = courier_data[0]
        password = courier_data[1]
        first_name = courier_data[2]
        
        yield login, password, first_name
        
        try:
            login_response = login_courier(login, password)
            if login_response.status_code == 200:
                courier_id = login_response.json()["id"]
                delete_courier(courier_id)
        except:
            pass  
    else:
        yield None, None, None