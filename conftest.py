import pytest
import requests
import allure
from helpers.courier_helpers import generate_random_string
from config import Endpoints
from test_data import TestData


@pytest.fixture
def created_courier():
    data = TestData.get_courier_data()
    login = data["login"]
    password = data["password"]
    first_name = data.get("firstName", "")
    
    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }
    
    url = Endpoints.get_full_url(Endpoints.COURIER)
    response = requests.post(url, data=payload)
    
    if response.status_code != 201:
        raise Exception(f"Не удалось создать курьера: {response.status_code}")
    
    yield login, password, first_name
    
    cleanup_courier(login, password)


@pytest.fixture
def created_courier_id():
    data = TestData.get_courier_data()
    login = data["login"]
    password = data["password"]
    
    payload = {
        "login": login,
        "password": password
    }
    
    url = Endpoints.get_full_url(Endpoints.COURIER)
    response = requests.post(url, data=payload)
    
    if response.status_code != 201:
        raise Exception(f"Не удалось создать курьера: {response.status_code}")
    
    login_payload = {"login": login, "password": password}
    login_url = Endpoints.get_full_url(Endpoints.COURIER_LOGIN)
    login_response = requests.post(login_url, data=login_payload)
    
    if login_response.status_code != 200:
        raise Exception(f"Не удалось авторизовать курьера: {login_response.status_code}")
    
    courier_id = login_response.json()["id"]
    
    yield courier_id
    
    delete_courier_by_id(courier_id)


@pytest.fixture
def cleanup_courier_fixture():
    couriers_to_cleanup = []
    
    yield couriers_to_cleanup
    
    for login, password in couriers_to_cleanup:
        cleanup_courier(login, password)


@pytest.fixture
def cleanup_courier_by_id_fixture():
    courier_ids_to_cleanup = []
    
    yield courier_ids_to_cleanup
    
    for courier_id in courier_ids_to_cleanup:
        delete_courier_by_id(courier_id)


def cleanup_courier(login, password):
    try:
        login_payload = {"login": login, "password": password}
        login_url = Endpoints.get_full_url(Endpoints.COURIER_LOGIN)
        login_response = requests.post(login_url, data=login_payload)
        
        if login_response.status_code == 200:
            courier_id = login_response.json()["id"]
            delete_url = Endpoints.get_full_url(
                Endpoints.COURIER_DELETE.format(courier_id=courier_id)
            )
            requests.delete(delete_url)
    except Exception as e:
        allure.attach(f"Ошибка при удалении курьера: {str(e)}",
                     "Игнорируем ошибку удаления")


def delete_courier_by_id(courier_id):
    try:
        delete_url = Endpoints.get_full_url(
            Endpoints.COURIER_DELETE.format(courier_id=courier_id)
        )
        requests.delete(delete_url)
    except Exception as e:
        allure.attach(f"Ошибка при удалении курьера ID {courier_id}: {str(e)}",
                     "Игнорируем ошибку удаления")