import requests
import random
import string
import allure


def generate_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


@allure.step("Регистрация нового курьера")
def register_new_courier_and_return_login_password():
    login_pass = []
    
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)
    
    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }
    
    response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier', data=payload)
    
    if response.status_code == 201:
        login_pass.append(login)
        login_pass.append(password)
        login_pass.append(first_name)
    
    return login_pass


@allure.step("Удаление курьера")
def delete_courier(courier_id):
    response = requests.delete(f'https://qa-scooter.praktikum-services.ru/api/v1/courier/{courier_id}')
    return response


@allure.step("Авторизация курьера")
def login_courier(login, password):
    payload = {"login": login, "password": password}
    response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier/login', data=payload)
    return response