import pytest
import requests
import allure
from helpers.courier_helpers import (
    register_new_courier_and_return_login_password,
    login_courier,
    delete_courier,
    generate_random_string
)


class TestAdditionalTasks:
    
    
    @allure.title("Доп.тест 1: Неуспешный запрос возвращает соответствующую ошибку")
    def test_delete_courier_with_invalid_id_fails(self):
        """Проверка удаления курьера с невалидным ID"""
        response = delete_courier("invalid_id")
        
        assert response.status_code in [400, 404, 500]
    
    @allure.title("Доп.тест 2: Успешный запрос возвращает ok true")
    def test_delete_courier_success_returns_ok_true(self):
        courier_data = register_new_courier_and_return_login_password()
        login, password, _ = courier_data
        
        login_response = login_courier(login, password)
        courier_id = login_response.json()["id"]
        
        response = delete_courier(courier_id)
        
        assert response.status_code == 200
        assert response.json() == {"ok": True}
    
    @allure.title("Доп.тест 3: Если отправить запрос без id, вернётся ошибка")
    def test_delete_courier_without_id_fails(self):
        response = requests.delete('https://qa-scooter.praktikum-services.ru/api/v1/courier/')
        
        assert response.status_code == 404 or response.status_code == 405
    
    @allure.title("Доп.тест 4: Если отправить запрос с несуществующим id, вернётся ошибка")
    def test_delete_nonexistent_courier_fails(self):
        response = delete_courier("999999")
        
        assert response.status_code in [400, 404]
        if response.status_code == 404:
            assert response.json()["message"] == "Курьера с таким id нет."
    
    
    @allure.title("Доп.тест 5: Успешный запрос возвращает ok true")
    def test_accept_order_success(self):
        courier_data = register_new_courier_and_return_login_password()
        login, password, _ = courier_data
        login_response = login_courier(login, password)
        courier_id = login_response.json()["id"]
        
        try:
            order_payload = {
                "firstName": "Test",
                "lastName": "User",
                "address": "Test address",
                "metroStation": 4,
                "phone": "+7 800 355 35 35",
                "rentTime": 5,
                "deliveryDate": "2020-06-06",
                "comment": "Test comment"
            }
            
            order_response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/orders', json=order_payload)
            
            assert order_response.status_code == 201
            order_data = order_response.json()
            assert "track" in order_data
            
            track = order_data["track"]
            track_response = requests.get(
                'https://qa-scooter.praktikum-services.ru/api/v1/orders/track',
                params={"t": track}
            )
            
            assert track_response.status_code == 200
            order_id = track_response.json()["order"]["id"]
            
            params = {"courierId": courier_id}
            response = requests.put(f'https://qa-scooter.praktikum-services.ru/api/v1/orders/accept/{order_id}', params=params)
            
            assert response.status_code == 200
            assert response.json() == {"ok": True}
        finally:
            delete_courier(courier_id)
    
    @allure.title("Доп.тест 6: Если не передать id курьера, запрос вернёт ошибку")
    def test_accept_order_without_courier_id_fails(self):
        response = requests.put('https://qa-scooter.praktikum-services.ru/api/v1/orders/accept/123')
        
        assert response.status_code == 400
        assert response.json()["message"] == "Недостаточно данных для поиска"
    
    @allure.title("Доп.тест 7: Если передать неверный id курьера, запрос вернёт ошибку")
    def test_accept_order_with_wrong_courier_id_fails(self):
        params = {"courierId": "999999"}
        response = requests.put('https://qa-scooter.praktikum-services.ru/api/v1/orders/accept/123', params=params)
        
        assert response.status_code == 404
        assert response.json()["message"] == "Курьера с таким id не существует"
    
    @allure.title("Доп.тест 8: Если не передать id заказа, запрос вернёт ошибку")
    def test_accept_order_without_order_id_fails(self):
        params = {"courierId": "123"}
        response = requests.put('https://qa-scooter.praktikum-services.ru/api/v1/orders/accept/', params=params)
        
        assert response.status_code == 404
    
    @allure.title("Доп.тест 9: Если передать неверный id заказа, запрос вернёт ошибку")
    def test_accept_order_with_wrong_order_id_fails(self):
        courier_data = register_new_courier_and_return_login_password()
        login, password, _ = courier_data
        login_response = login_courier(login, password)
        courier_id = login_response.json()["id"]
        
        try:
            params = {"courierId": courier_id}
            response = requests.put('https://qa-scooter.praktikum-services.ru/api/v1/orders/accept/999999', params=params)
            
            assert response.status_code == 404
            assert response.json()["message"] == "Заказа с таким id не существует"
        finally:
            delete_courier(courier_id)
    
    
    @allure.title("Доп.тест 10: Успешный запрос возвращает объект с заказом")
    def test_get_order_by_track_success(self):
        payload = {
            "firstName": "Test",
            "lastName": "User",
            "address": "Test address",
            "metroStation": 4,
            "phone": "+7 800 355 35 35",
            "rentTime": 5,
            "deliveryDate": "2020-06-06",
            "comment": "Test comment"
        }
        
        order_response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/orders', json=payload)
        track = order_response.json()["track"]
        
        params = {"t": track}
        response = requests.get('https://qa-scooter.praktikum-services.ru/api/v1/orders/track', params=params)
        
        assert response.status_code == 200
        response_data = response.json()
        assert "order" in response_data
        order = response_data["order"]
        assert "id" in order
        assert "track" in order
        assert order["track"] == track
    
    @allure.title("Доп.тест 11: Запрос без номера заказа возвращает ошибку")
    def test_get_order_without_track_fails(self):
        response = requests.get('https://qa-scooter.praktikum-services.ru/api/v1/orders/track')
        
        assert response.status_code == 400
        assert response.json()["message"] == "Недостаточно данных для поиска"
    
    @allure.title("Доп.тест 12: Запрос с несуществующим заказом возвращает ошибку")
    def test_get_nonexistent_order_fails(self):
        params = {"t": "999999"}
        response = requests.get('https://qa-scooter.praktikum-services.ru/api/v1/orders/track', params=params)
        
        assert response.status_code == 404
        assert response.json()["message"] == "Заказ не найден"