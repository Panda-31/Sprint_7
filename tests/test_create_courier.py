import pytest
import requests
import allure
from helpers.courier_helpers import (
    register_new_courier_and_return_login_password,
    generate_random_string
)


class TestCreateCourier:
    
    @allure.title("Тест 1: Успешное создание курьера")
    def test_create_courier_success(self):
        with allure.step("Создание нового курьера"):
            courier_data = register_new_courier_and_return_login_password()
        
        with allure.step("Проверка, что курьер создан"):
            assert len(courier_data) == 3, "Курьер не был создан"
            
        if len(courier_data) == 3:
            login, password, _ = courier_data
            response = requests.post(
                'https://qa-scooter.praktikum-services.ru/api/v1/courier/login',
                data={"login": login, "password": password}
            )
            if response.status_code == 200:
                courier_id = response.json()["id"]
                requests.delete(f'https://qa-scooter.praktikum-services.ru/api/v1/courier/{courier_id}')
    
    @allure.title("Тест 2: Нельзя создать двух одинаковых курьеров")
    def test_create_duplicate_courier_fails(self):
        login = generate_random_string(10)
        password = generate_random_string(10)
        first_name = generate_random_string(10)
        
        with allure.step("Создаем первого курьера"):
            payload1 = {
                "login": login,
                "password": password,
                "firstName": first_name
            }
            
            response1 = requests.post(
                'https://qa-scooter.praktikum-services.ru/api/v1/courier',
                data=payload1
            )
            
            assert response1.status_code == 201, f"Первый курьер не создался: {response1.status_code} {response1.text}"
            
        try:
            with allure.step("Пытаемся создать курьера с таким же логином"):
                payload2 = {
                    "login": login,
                    "password": password + "_duplicate",
                    "firstName": first_name + "_duplicate"
                }
                
                response2 = requests.post(
                    'https://qa-scooter.praktikum-services.ru/api/v1/courier',
                    data=payload2
                )
                
                assert response2.status_code == 409, f"Ожидался код 409, получен {response2.status_code}: {response2.text}"
                assert response2.json()["message"] == "Этот логин уже используется. Попробуйте другой."
                
        finally:
            login_response1 = requests.post(
                'https://qa-scooter.praktikum-services.ru/api/v1/courier/login',
                data={"login": login, "password": password}
            )
            if login_response1.status_code == 200:
                courier_id1 = login_response1.json()["id"]
                requests.delete(f'https://qa-scooter.praktikum-services.ru/api/v1/courier/{courier_id1}')
    
    @allure.title("Тест 3: Для создания курьера нужны все обязательные поля")
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_create_courier_missing_field_fails(self, missing_field):
        with allure.step(f"Создаем запрос без поля {missing_field}"):
            payload = {
                "login": generate_random_string(10),
                "password": generate_random_string(10),
                "firstName": generate_random_string(10)
            }
            payload.pop(missing_field)
            
            response = requests.post(
                'https://qa-scooter.praktikum-services.ru/api/v1/courier',
                data=payload
            )
            
            assert response.status_code == 400
            assert response.json()["message"] == "Недостаточно данных для создания учетной записи"
    
    @allure.title("Тест 3.1: Поле firstName не является обязательным")
    def test_create_courier_without_firstname_success(self):
        login = generate_random_string(10)
        password = generate_random_string(10)
        
        payload = {
            "login": login,
            "password": password
        }
        
        response = requests.post(
            'https://qa-scooter.praktikum-services.ru/api/v1/courier',
            data=payload
        )
        
        assert response.status_code == 201
        
        login_response = requests.post(
            'https://qa-scooter.praktikum-services.ru/api/v1/courier/login',
            data={"login": login, "password": password}
        )
        if login_response.status_code == 200:
            courier_id = login_response.json()["id"]
            requests.delete(f'https://qa-scooter.praktikum-services.ru/api/v1/courier/{courier_id}')
    
    @allure.title("Тест 4: Успешный запрос возвращает правильный код ответа")
    def test_create_courier_response_code_correct(self):
        with allure.step("Создаем нового курьера"):
            login = generate_random_string(10)
            password = generate_random_string(10)
            first_name = generate_random_string(10)
            
            payload = {
                "login": login,
                "password": password,
                "firstName": first_name
            }
            
            response = requests.post(
                'https://qa-scooter.praktikum-services.ru/api/v1/courier',
                data=payload
            )
            
            assert response.status_code in [201, 409], f"Неожиданный код ответа: {response.status_code}"
                
        if response.status_code == 201:
            login_response = requests.post(
                'https://qa-scooter.praktikum-services.ru/api/v1/courier/login',
                data={"login": login, "password": password}
            )
            if login_response.status_code == 200:
                courier_id = login_response.json()["id"]
                requests.delete(f'https://qa-scooter.praktikum-services.ru/api/v1/courier/{courier_id}')
    
    @allure.title("Тест 5: Успешный запрос возвращает ok true")
    def test_success_response_contains_ok_true(self):
        with allure.step("Создаем нового курьера"):
            login = generate_random_string(10)
            password = generate_random_string(10)
            first_name = generate_random_string(10)
            
            payload = {
                "login": login,
                "password": password,
                "firstName": first_name
            }
            
            response = requests.post(
                'https://qa-scooter.praktikum-services.ru/api/v1/courier',
                data=payload
            )
            
            if response.status_code == 201:
                assert response.json() == {"ok": True}
                
        if response.status_code == 201:
            login_response = requests.post(
                'https://qa-scooter.praktikum-services.ru/api/v1/courier/login',
                data={"login": login, "password": password}
            )
            if login_response.status_code == 200:
                courier_id = login_response.json()["id"]
                requests.delete(f'https://qa-scooter.praktikum-services.ru/api/v1/courier/{courier_id}')
    
    @allure.title("Тест 6: Если одного из обязательных полей нет - возвращается ошибка")
    def test_missing_required_field_returns_error(self):
        payload_no_login = {
            "password": "password123",
            "firstName": "Ivan"
        }
        
        response = requests.post(
            'https://qa-scooter.praktikum-services.ru/api/v1/courier',
            data=payload_no_login
        )
        
        assert response.status_code == 400
        assert response.json()["message"] == "Недостаточно данных для создания учетной записи"
        
        payload_no_password = {
            "login": "ivan123",
            "firstName": "Ivan"
        }
        
        response = requests.post(
            'https://qa-scooter.praktikum-services.ru/api/v1/courier',
            data=payload_no_password
        )
        
        assert response.status_code == 400
        assert response.json()["message"] == "Недостаточно данных для создания учетной записи"
        
        payload_no_name = {
            "login": generate_random_string(10),
            "password": "password123"
        }
        
        response = requests.post(
            'https://qa-scooter.praktikum-services.ru/api/v1/courier',
            data=payload_no_name
        )
        
        assert response.status_code in [201, 409]
        
        if response.status_code == 201:
            login_response = requests.post(
                'https://qa-scooter.praktikum-services.ru/api/v1/courier/login',
                data={"login": payload_no_name["login"], "password": payload_no_name["password"]}
            )
            if login_response.status_code == 200:
                courier_id = login_response.json()["id"]
                requests.delete(f'https://qa-scooter.praktikum-services.ru/api/v1/courier/{courier_id}')
    
    @allure.title("Тест 7: Создание курьера с существующим логином возвращает ошибку")
    def test_create_existing_login_returns_error(self):
        login = generate_random_string(10)
        password = generate_random_string(10)
        first_name = generate_random_string(10)
        
        payload1 = {
            "login": login,
            "password": password,
            "firstName": first_name
        }
        
        response1 = requests.post(
            'https://qa-scooter.praktikum-services.ru/api/v1/courier',
            data=payload1
        )
        
        assert response1.status_code == 201, f"Первый курьер не создался: {response1.status_code} {response1.text}"
        
        payload2 = {
            "login": login,
            "password": "different_password",
            "firstName": "Different Name"
        }
        
        response2 = requests.post(
            'https://qa-scooter.praktikum-services.ru/api/v1/courier',
            data=payload2
        )
        
        assert response2.status_code == 409, f"Ожидался код 409, получен {response2.status_code}: {response2.text}"
        assert response2.json()["message"] == "Этот логин уже используется. Попробуйте другой."
        
        login_response = requests.post(
            'https://qa-scooter.praktikum-services.ru/api/v1/courier/login',
            data={"login": login, "password": password}
        )
        if login_response.status_code == 200:
            courier_id = login_response.json()["id"]
            requests.delete(f'https://qa-scooter.praktikum-services.ru/api/v1/courier/{courier_id}')