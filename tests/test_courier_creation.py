import allure
import pytest
import requests
from data import *


class TestCourierCreation:
    @allure.title('Успешное создание курьера')
    @allure.description('''
    Покрываем требования:
    1. Курьера можно создать
    4. Запрос возвращает правильный код ответа (201)
    5. Успешный запрос возвращает {"ok": true}
    ''')
    def test_create_courier_success(self, generate_courier_data_and_cleanup):
        with allure.step("Создать нового курьера"):
            response = requests.post(CREATE_COURIER_URL, json=generate_courier_data_and_cleanup)

        with allure.step("Проверить ответ на создание курьера"):
            assert response.status_code == HTTP_201
            assert response.json() == SUCCESS_CREATION_RESPONSE


    @allure.title('Ошибка при дубликате логина')
    @allure.description('''
    Покрываем требования:
    2. Нельзя создать двух одинаковых курьеров
    4. Запрос возвращает правильный код ответа (409)
    7. При создании с существующим логином возвращается ошибка
    ''')
    def test_create_duplicate_courier_error(self, generate_courier_data_and_cleanup):
        with allure.step("Создать первого курьера"):
            first_response = requests.post(CREATE_COURIER_URL, json=generate_courier_data_and_cleanup)
            assert first_response.status_code == HTTP_201

        with allure.step("Попытаться создать дубликат курьера"):
            duplicate_response = requests.post(CREATE_COURIER_URL, json=generate_courier_data_and_cleanup)

        with allure.step("Проверить ошибку дубликата"):
            assert duplicate_response.status_code == HTTP_409
            assert duplicate_response.json() == DUPLICATE_LOGIN_RESPONSE


    @allure.title('Ошибка при отсутствии обязательных полей')
    @allure.description('''
    Покрываем требования:
    3. Для создания нужны все обязательные поля (login, password)
    4. Запрос возвращает правильный код ответа (400)
    6. При отсутствии полей возвращается ошибка
    ''')
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_create_courier_missing_field_error(self, generate_courier_data_and_cleanup, missing_field):
        with allure.step("Подготовить данные без обязательного поля"):
            payload = generate_courier_data_and_cleanup.copy()
            payload.pop(missing_field)

        with allure.step("Отправить запрос с неполными данными"):
            response = requests.post(CREATE_COURIER_URL, json=payload)

        with allure.step("Проверить ошибку валидации"):
            assert response.status_code == HTTP_400
            assert MISSING_FIELD_RESPONSE["message"] in response.json().get("message")
