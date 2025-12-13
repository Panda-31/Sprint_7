import pytest
import requests
import allure
from helpers.courier_helpers import generate_random_string
from config import Endpoints


@pytest.fixture
def created_courier():
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)
    
    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }
    
    url = Endpoints.get_full_url(Endpoints.COURIER)
    response = requests.post(url, data=payload)
    
    assert response.status_code == 201, f"Не удалось создать курьера: {response.status_code}"
    
    yield login, password, first_name
    
    try:
        login_payload = {"login": login, "password": password}
        login_url = Endpoints.get_full_url(Endpoints.COURIER_LOGIN)
        login_response = requests.post(login_url, data=login_payload)
        
        if login_response.status_code == 200:
            courier_id = login_response.json()["id"]
            delete_url = Endpoints.get_full_url(
                Endpoints.COURIER_DELETE.format(courier_id=courier_id)
            )
            delete_response = requests.delete(delete_url)
            if delete_response.status_code != 200:
                allure.attach(f"Не удалось удалить курьера {courier_id}",
                            f"Код ответа: {delete_response.status_code}")
    except Exception as e:
        allure.attach(f"Ошибка при удалении курьера: {str(e)}",
                     "Игнорируем ошибку удаления для продолжения тестов")