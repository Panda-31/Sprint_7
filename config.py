BASE_URL = "https://qa-scooter.praktikum-services.ru"


class Endpoints:
    COURIER = "/api/v1/courier"
    COURIER_LOGIN = "/api/v1/courier/login"
    COURIER_DELETE = "/api/v1/courier/{courier_id}"
    
    ORDERS = "/api/v1/orders"
    ORDER_TRACK = "/api/v1/orders/track"
    ORDER_ACCEPT = "/api/v1/orders/accept/{order_id}"
    
    @staticmethod
    def get_full_url(endpoint):
        return BASE_URL + endpoint