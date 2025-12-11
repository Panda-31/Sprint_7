import requests
import allure


class TestGetOrdersList:
    
    @allure.title("Получение списка заказов")
    def test_get_orders_list_returns_list(self):
        response = requests.get('https://qa-scooter.praktikum-services.ru/api/v1/orders')
        
        assert response.status_code == 200
        assert "orders" in response.json()
        assert isinstance(response.json()["orders"], list)