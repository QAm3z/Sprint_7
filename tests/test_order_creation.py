import allure
import pytest
import requests
from data import *


class TestOrderCreation:
    @allure.title('Создание заказа с разными цветами')
    @allure.description('''
    Проверяем что:
    - Можно указать BLACK или GREY
    - Можно указать оба цвета
    - Можно не указывать цвет
    - Ответ содержит track
    ''')
    @pytest.mark.parametrize('colors', [
        ['BLACK'],
        ['GREY'],
        ['BLACK', 'GREY'],
        []
    ])
    def test_create_order_with_colors(self, generate_order_data, colors):
        with allure.step("Подготовить данные заказа"):
            order_data = generate_order_data.copy()
            order_data['color'] = colors

        with allure.step("Отправить запрос на создание заказа"):
            response = requests.post(CREATE_ORDER_URL, json=order_data)

        with allure.step("Проверить успешное создание"):
            assert response.status_code == HTTP_201
            assert all(key in response.json() for key in SUCCESS_ORDER_RESPONSE_KEYS)
