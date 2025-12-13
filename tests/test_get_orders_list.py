import requests
import allure
from config import Endpoints


class TestGetOrdersList:
    
    @allure.title("Тест получения списка заказов")
    def test_get_orders_list_returns_list(self):
        with allure.step("Отправка запроса на получение списка заказов"):
            url = Endpoints.get_full_url(Endpoints.ORDERS)
            response = requests.get(url)
        
        with allure.step("Проверка успешного получения списка"):
            assert response.status_code == 200, f"Ожидался код 200, получен {response.status_code}"
            
            response_data = response.json()
            assert "orders" in response_data, "Ответ не содержит ключа 'orders'"
            assert isinstance(response_data["orders"], list), "Orders не является списком"