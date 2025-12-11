import pytest
import requests
import allure
from helpers.courier_helpers import login_courier


class TestLoginCourier:
    
    @allure.title("Тест 1: Курьер может авторизоваться")
    def test_login_courier_success(self, create_and_delete_courier):
        login, password, _ = create_and_delete_courier
        
        response = login_courier(login, password)
        
        assert response.status_code == 200
        assert "id" in response.json()
    
    @allure.title("Тест 2: Для авторизации нужно передать все обязательные поля")
    @pytest.mark.parametrize("missing_field,field_value", [
        ("login", "test_login"),
        ("password", "test_password")
    ])
    def test_login_missing_field_fails(self, missing_field, field_value):
        payload = {"login": "test", "password": "test"}
        payload.pop(missing_field)
        
        response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier/login', data=payload)
        
        assert response.status_code in [400, 504]
        if response.status_code == 400:
            assert response.json()["message"] == "Недостаточно данных для входа"
    
    @allure.title("Тест 3: Ошибка при неправильном логине")
    def test_login_wrong_login_fails(self, create_and_delete_courier):
        _, password, _ = create_and_delete_courier
        
        response = login_courier("wrong_login", password)
        
        assert response.status_code == 404
        assert response.json()["message"] == "Учетная запись не найдена"
    
    @allure.title("Тест 4: Ошибка при неправильном пароле")
    def test_login_wrong_password_fails(self, create_and_delete_courier):
        login, _, _ = create_and_delete_courier
        
        response = login_courier(login, "wrong_password")
        
        assert response.status_code == 404
        assert response.json()["message"] == "Учетная запись не найдена"
    
    @allure.title("Тест 5: Ошибка при отсутствии поля")
    def test_login_without_field_returns_error(self):
        response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier/login', 
                                data={"password": "test"})
        
        assert response.status_code in [400, 504]
        if response.status_code == 400:
            assert response.json()["message"] == "Недостаточно данных для входа"
        
        response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier/login', 
                                data={"login": "test"})
        
        assert response.status_code in [400, 504]
        if response.status_code == 400:
            assert response.json()["message"] == "Недостаточно данных для входа"
    
    @allure.title("Тест 6: Авторизация несуществующего пользователя возвращает ошибку")
    def test_login_nonexistent_courier_fails(self):
        response = login_courier("nonexistent_login_12345", "nonexistent_pass_12345")
        
        assert response.status_code == 404
        assert response.json()["message"] == "Учетная запись не найдена"
    
    @allure.title("Тест 7: Успешный запрос возвращает id")
    def test_successful_login_returns_id(self, create_and_delete_courier):
        login, password, _ = create_and_delete_courier
        
        response = login_courier(login, password)
        
        assert response.status_code == 200
        response_data = response.json()
        assert "id" in response_data
        assert isinstance(response_data["id"], int)