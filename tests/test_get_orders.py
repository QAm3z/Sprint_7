import allure
import pytest
import requests
from data import *


class TestGetOrders:
    @allure.title('Проверка списка заказов')
    @allure.description('Проверяем что возвращается непустой список заказов')
    def test_get_orders_list(self):
        with allure.step("Запросить список заказов"):
            response = requests.get(GET_ORDERS_URL)
            data = response.json()

        with allure.step("Проверить ответ сервера"):
            assert response.status_code == HTTP_200
            assert isinstance(data['orders'], list)
            assert data['orders']
