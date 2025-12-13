import pytest
import requests
import allure
from helpers.courier_helpers import create_order
from config import Endpoints


class TestCreateOrder:
    
    @allure.title("Тест создания заказа с цветом BLACK")
    def test_create_order_with_black_color(self):
        with allure.step("Создание заказа с цветом BLACK"):
            response = create_order(["BLACK"])
        
        with allure.step("Проверка успешного создания заказа"):
            assert response.status_code == 201, f"Ожидался код 201, получен {response.status_code}"
            assert "track" in response.json(), "Ответ не содержит track номера"
            assert isinstance(response.json()["track"], int), "Track не является числом"
    
    @allure.title("Тест создания заказа с цветом GREY")
    def test_create_order_with_grey_color(self):
        with allure.step("Создание заказа с цветом GREY"):
            response = create_order(["GREY"])
        
        with allure.step("Проверка успешного создания заказа"):
            assert response.status_code == 201, f"Ожидался код 201, получен {response.status_code}"
            assert "track" in response.json(), "Ответ не содержит track номера"
            assert isinstance(response.json()["track"], int), "Track не является числом"
    
    @allure.title("Тест создания заказа с обоими цветами")
    def test_create_order_with_both_colors(self):
        with allure.step("Создание заказа с обоими цветами"):
            response = create_order(["BLACK", "GREY"])
        
        with allure.step("Проверка успешного создания заказа"):
            assert response.status_code == 201, f"Ожидался код 201, получен {response.status_code}"
            assert "track" in response.json(), "Ответ не содержит track номера"
            assert isinstance(response.json()["track"], int), "Track не является числом"
    
    @allure.title("Тест создания заказа без указания цвета")
    def test_create_order_without_color(self):
        with allure.step("Создание заказа без указания цвета"):
            response = create_order()
        
        with allure.step("Проверка успешного создания заказа"):
            assert response.status_code == 201, f"Ожидался код 201, получен {response.status_code}"
            assert "track" in response.json(), "Ответ не содержит track номера"
            assert isinstance(response.json()["track"], int), "Track не является числом"