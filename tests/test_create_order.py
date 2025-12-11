import pytest
import requests
import allure


class TestCreateOrder:
    
    @staticmethod
    def _create_order(color=None):
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
            
        response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/orders', json=payload)
        return response
    
    @allure.title("Тест 1: Создание заказа с цветом BLACK")
    def test_create_order_with_black_color(self):
        response = self._create_order(["BLACK"])
        
        assert response.status_code == 201
        assert "track" in response.json()
        assert isinstance(response.json()["track"], int)
    
    @allure.title("Тест 2: Создание заказа с цветом GREY")
    def test_create_order_with_grey_color(self):
        response = self._create_order(["GREY"])
        
        assert response.status_code == 201
        assert "track" in response.json()
        assert isinstance(response.json()["track"], int)
    
    @allure.title("Тест 3: Создание заказа с обоими цветами")
    def test_create_order_with_both_colors(self):
        response = self._create_order(["BLACK", "GREY"])
        
        assert response.status_code == 201
        assert "track" in response.json()
        assert isinstance(response.json()["track"], int)
    
    @allure.title("Тест 4: Создание заказа без указания цвета")
    def test_create_order_without_color(self):
        response = self._create_order()
        
        assert response.status_code == 201
        assert "track" in response.json()
        assert isinstance(response.json()["track"], int)
    
    @allure.title("Тест 5: Параметризованный тест создания заказа")
    @pytest.mark.parametrize("color", [
        ["BLACK"],
        ["GREY"],
        ["BLACK", "GREY"],
        None
    ])
    def test_create_order_parametrized(self, color):
        response = self._create_order(color)
        
        assert response.status_code == 201
        response_data = response.json()
        assert "track" in response_data
        assert isinstance(response_data["track"], int)