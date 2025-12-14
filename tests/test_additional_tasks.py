import pytest
import requests
import allure
from test_data import TestData
from config import Endpoints
from helpers.courier_helpers import register_courier


class TestAdditionalTasks:
    
    @allure.title("Тест успешного удаления курьера")
    def test_delete_courier_success_returns_ok_true(self, created_courier_id):
        courier_id = created_courier_id
        
        with allure.step("Отправка запроса на удаление курьера"):
            delete_url = Endpoints.get_full_url(Endpoints.COURIER_DELETE.format(courier_id=courier_id))
            response = requests.delete(delete_url)
        
        with allure.step("Проверка успешного удаления"):
            assert response.status_code == 200, f"Ожидался код 200, получен {response.status_code}"
            assert response.json() == {"ok": True}, "Ответ не содержит {'ok': true}"
    
    @allure.title("Тест удаления курьера с несуществующим ID")
    def test_delete_nonexistent_courier_fails(self):
        non_existent_id = 999999
        
        with allure.step("Отправка запроса на удаление несуществующего курьера"):
            url = Endpoints.get_full_url(Endpoints.COURIER_DELETE.format(courier_id=non_existent_id))
            response = requests.delete(url)
        
        with allure.step("Проверка ошибки удаления"):
            assert response.status_code == 404, f"Ожидался код 404, получен {response.status_code}"
    
    @allure.title("Тест принятия заказа без ID курьера")
    def test_accept_order_without_courier_id_fails(self):
        with allure.step("Отправка запроса на принятие заказа без ID курьера"):
            url = Endpoints.get_full_url(Endpoints.ORDER_ACCEPT.format(order_id=123))
            response = requests.put(url)
        
        with allure.step("Проверка ошибки валидации"):
            assert response.status_code == 400, f"Ожидался код 400, получен {response.status_code}"
            assert response.json()["message"] == "Недостаточно данных для поиска"
    
    @allure.title("Тест принятия заказа с неверным ID курьера")
    def test_accept_order_with_wrong_courier_id_fails(self):
        with allure.step("Подготовка параметров с неверным ID курьера"):
            params = {"courierId": "999999"}
        
        with allure.step("Отправка запроса на принятие заказа с неверным ID курьера"):
            url = Endpoints.get_full_url(Endpoints.ORDER_ACCEPT.format(order_id=123))
            response = requests.put(url, params=params)
        
        with allure.step("Проверка ошибки поиска курьера"):
            assert response.status_code == 404, f"Ожидался код 404, получен {response.status_code}"
            assert response.json()["message"] == "Курьера с таким id не существует"
    
    @allure.title("Тест принятия заказа с неверным ID заказа")
    def test_accept_order_with_wrong_order_id_fails(self, created_courier_id):
        courier_id = created_courier_id
        
        with allure.step("Подготовка параметров"):
            params = {"courierId": courier_id}
        
        with allure.step("Отправка запроса на принятие несуществующего заказа"):
            url = Endpoints.get_full_url(Endpoints.ORDER_ACCEPT.format(order_id=999999))
            response = requests.put(url, params=params)
        
        with allure.step("Проверка ошибки поиска заказа"):
            assert response.status_code == 404, f"Ожидался код 404, получен {response.status_code}"
            assert response.json()["message"] == "Заказа с таким id не существует"
    
    @allure.title("Тест получения заказа по номеру")
    def test_get_order_by_track_success(self):
        payload = TestData.get_order_data()
        
        with allure.step("Создание заказа"):
            url = Endpoints.get_full_url(Endpoints.ORDERS)
            order_response = requests.post(url, json=payload)
            
            track = order_response.json()["track"]
        
        with allure.step("Подготовка параметров поиска"):
            params = {"t": track}
        
        with allure.step("Отправка запроса на получение заказа по track"):
            url = Endpoints.get_full_url(Endpoints.ORDER_TRACK)
            response = requests.get(url, params=params)
        
        with allure.step("Проверка успешного получения заказа"):
            assert response.status_code == 200, f"Ожидался код 200, получен {response.status_code}"
            
            response_data = response.json()
            assert "order" in response_data, "Ответ не содержит ключа 'order'"
            
            order = response_data["order"]
            assert "id" in order, "Заказ не содержит id"
            assert "track" in order, "Заказ не содержит track"
            assert order["track"] == track, "Track номер не совпадает"
    
    @allure.title("Тест получения заказа без номера")
    def test_get_order_without_track_fails(self):
        with allure.step("Отправка запроса на получение заказа без номера"):
            url = Endpoints.get_full_url(Endpoints.ORDER_TRACK)
            response = requests.get(url)
        
        with allure.step("Проверка ошибки валидации"):
            assert response.status_code == 400, f"Ожидался код 400, получен {response.status_code}"
            assert response.json()["message"] == "Недостаточно данных для поиска"
    
    @allure.title("Тест получения несуществующего заказа")
    def test_get_nonexistent_order_fails(self):
        with allure.step("Подготовка параметров с несуществующим track"):
            params = {"t": "999999"}
        
        with allure.step("Отправка запроса на получение несуществующего заказа"):
            url = Endpoints.get_full_url(Endpoints.ORDER_TRACK)
            response = requests.get(url, params=params)
        
        with allure.step("Проверка ошибки поиска заказа"):
            assert response.status_code == 404, f"Ожидался код 404, получен {response.status_code}"
            assert response.json()["message"] == "Заказ не найден"