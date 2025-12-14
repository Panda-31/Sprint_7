import pytest
import requests
import allure
from test_data import TestData
from config import Endpoints


class TestCreateCourier:
    
    @allure.title("Тест успешного создания курьера")
    def test_create_courier_success(self, cleanup_courier_fixture):
        data = TestData.get_courier_data()
        
        with allure.step("Подготовка данных для создания курьера"):
            payload = data
        
        with allure.step("Отправка запроса на создание курьера"):
            url = Endpoints.get_full_url(Endpoints.COURIER)
            response = requests.post(url, data=payload)
        
        with allure.step("Проверка, что курьер создан успешно"):
            assert response.status_code == 201, f"Ожидался код 201, получен {response.status_code}"
            assert response.json() == {"ok": True}, "Ответ не содержит {'ok': true}"
        
        cleanup_courier_fixture.append((data["login"], data["password"]))
    
    @allure.title("Тест создания курьера с дублирующимся логином")
    def test_create_duplicate_courier_fails(self, created_courier):
        login, password, first_name = created_courier
        
        with allure.step("Подготовка данных для создания дубликата"):
            payload = {
                "login": login,
                "password": "different_password",
                "firstName": "Different Name"
            }
        
        with allure.step("Отправка запроса на создание дубликата курьера"):
            url = Endpoints.get_full_url(Endpoints.COURIER)
            response = requests.post(url, data=payload)
        
        with allure.step("Проверка, что дубликат не создан"):
            assert response.status_code == 409, f"Ожидался код 409, получен {response.status_code}"
            assert response.json()["message"] == "Этот логин уже используется. Попробуйте другой."
    
    @allure.title("Тест создания курьера без логина")
    def test_create_courier_without_login_fails(self):
        with allure.step("Подготовка данных без поля login"):
            payload = {
                "password": TestData.get_courier_data()["password"],
                "firstName": TestData.get_courier_data()["firstName"]
            }
        
        with allure.step("Отправка запроса без поля login"):
            url = Endpoints.get_full_url(Endpoints.COURIER)
            response = requests.post(url, data=payload)
        
        with allure.step("Проверка ошибки валидации"):
            assert response.status_code == 400, f"Ожидался код 400, получен {response.status_code}"
            assert response.json()["message"] == "Недостаточно данных для создания учетной записи"
    
    @allure.title("Тест создания курьера без пароля")
    def test_create_courier_without_password_fails(self):
        with allure.step("Подготовка данных без поля password"):
            payload = {
                "login": TestData.get_courier_data()["login"],
                "firstName": TestData.get_courier_data()["firstName"]
            }
        
        with allure.step("Отправка запроса без поля password"):
            url = Endpoints.get_full_url(Endpoints.COURIER)
            response = requests.post(url, data=payload)
        
        with allure.step("Проверка ошибки валидации"):
            assert response.status_code == 400, f"Ожидался код 400, получен {response.status_code}"
            assert response.json()["message"] == "Недостаточно данных для создания учетной записи"
    
    @allure.title("Тест создания курьера без поля firstName")
    def test_create_courier_without_firstname_success(self, cleanup_courier_fixture):
        data = TestData.get_courier_data_without_firstname()
        
        with allure.step("Подготовка данных без поля firstName"):
            payload = data
        
        with allure.step("Отправка запроса без поля firstName"):
            url = Endpoints.get_full_url(Endpoints.COURIER)
            response = requests.post(url, data=payload)
        
        with allure.step("Проверка успешного создания"):
            assert response.status_code == 201, f"Ожидался код 201, получен {response.status_code}"
            assert response.json() == {"ok": True}, "Ответ не содержит {'ok': true}"
        
        cleanup_courier_fixture.append((data["login"], data["password"]))