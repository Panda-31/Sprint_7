import pytest
import requests
import allure
from helpers.courier_helpers import generate_random_string
from config import Endpoints


class TestLoginCourier:
    
    @allure.title("Тест успешной авторизации курьера")
    def test_login_courier_success(self, created_courier):
        login, password, _ = created_courier
        
        with allure.step("Подготовка данных для авторизации"):
            payload = {
                "login": login,
                "password": password
            }
        
        with allure.step("Отправка запроса на авторизацию"):
            url = Endpoints.get_full_url(Endpoints.COURIER_LOGIN)
            response = requests.post(url, data=payload)
        
        with allure.step("Проверка успешной авторизации"):
            assert response.status_code == 200, f"Ожидался код 200, получен {response.status_code}"
            assert "id" in response.json(), "Ответ не содержит id курьера"
    
    @allure.title("Тест авторизации с неверным логином")
    def test_login_with_wrong_login_fails(self, created_courier):
        _, password, _ = created_courier
        
        with allure.step("Подготовка данных с неверным логином"):
            payload = {
                "login": "wrong_login_" + generate_random_string(5),
                "password": password
            }
        
        with allure.step("Отправка запроса с неверным логином"):
            url = Endpoints.get_full_url(Endpoints.COURIER_LOGIN)
            response = requests.post(url, data=payload)
        
        with allure.step("Проверка ошибки авторизации"):
            assert response.status_code == 404, f"Ожидался код 404, получен {response.status_code}"
            assert response.json()["message"] == "Учетная запись не найдена"
    
    @allure.title("Тест авторизации с неверным паролем")
    def test_login_with_wrong_password_fails(self, created_courier):
        login, _, _ = created_courier
        
        with allure.step("Подготовка данных с неверным паролем"):
            payload = {
                "login": login,
                "password": "wrong_password_" + generate_random_string(5)
            }
        
        with allure.step("Отправка запроса с неверным паролем"):
            url = Endpoints.get_full_url(Endpoints.COURIER_LOGIN)
            response = requests.post(url, data=payload)
        
        with allure.step("Проверка ошибки авторизации"):
            assert response.status_code == 404, f"Ожидался код 404, получен {response.status_code}"
            assert response.json()["message"] == "Учетная запись не найдена"
    
    @allure.title("Тест авторизации без логина")
    def test_login_without_login_fails(self, created_courier):
        _, password, _ = created_courier
        
        with allure.step("Подготовка данных без поля login"):
            payload = {
                "password": password
            }
        
        with allure.step("Отправка запроса без поля login"):
            url = Endpoints.get_full_url(Endpoints.COURIER_LOGIN)
            response = requests.post(url, data=payload)
        
        with allure.step("Проверка ошибки валидации"):
            assert response.status_code == 400, f"Ожидался код 400, получен {response.status_code}"
            assert response.json()["message"] == "Недостаточно данных для входа"
    
    @allure.title("Тест авторизации без пароля - ожидается 400 Bad Request")
    @pytest.mark.xfail(reason="API иногда возвращает 504 Gateway Timeout вместо 400 Bad Request")
    def test_login_without_password_fails(self, created_courier):
        login, _, _ = created_courier
        
        with allure.step("Подготовка данных без поля password"):
            payload = {
                "login": login
            }
        
        with allure.step("Отправка запроса без поля password"):
            url = Endpoints.get_full_url(Endpoints.COURIER_LOGIN)
            response = requests.post(url, data=payload)
        
        with allure.step("Проверка ошибки валидации (ожидается 400)"):
            assert response.status_code == 400, f"Ожидался код 400, получен {response.status_code}"
            assert response.json()["message"] == "Недостаточно данных для входа"
    
    @allure.title("Тест авторизации несуществующего курьера")
    def test_login_nonexistent_courier_fails(self):
        with allure.step("Подготовка данных несуществующего курьера"):
            payload = {
                "login": "nonexistent_" + generate_random_string(10),
                "password": "nonexistent_" + generate_random_string(10)
            }
        
        with allure.step("Отправка запроса на авторизацию несуществующего курьера"):
            url = Endpoints.get_full_url(Endpoints.COURIER_LOGIN)
            response = requests.post(url, data=payload)
        
        with allure.step("Проверка ошибки авторизации"):
            assert response.status_code == 404, f"Ожидался код 404, получен {response.status_code}"
            assert response.json()["message"] == "Учетная запись не найдена"