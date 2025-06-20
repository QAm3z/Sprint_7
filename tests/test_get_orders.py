import allure
import pytest
import requests
from data import *


class TestGetOrders:
    @allure.title('Проверка списка заказов')
    @allure.description('Проверяем что возвращается непустой список заказов')
    def test_get_orders_list(self):
        response = requests.get(GET_ORDERS_URL)
        data = response.json()

        assert response.status_code == 200
        assert isinstance(data['orders'], list)
        assert data['orders']
