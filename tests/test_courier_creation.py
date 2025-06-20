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
        response = requests.post(CREATE_COURIER_URL, json=generate_courier_data_and_cleanup)

        assert response.status_code == 201
        assert response.json() == {"ok": True}

        login_response = requests.post(
            LOGIN_COURIER_URL,
            json={
                "login": generate_courier_data_and_cleanup["login"],
                "password": generate_courier_data_and_cleanup["password"]
            }
        )

        assert login_response.status_code == 200
        assert "id" in login_response.json()


    @allure.title('Ошибка при дубликате логина')
    @allure.description('''
    Покрываем требования:
    2. Нельзя создать двух одинаковых курьеров
    4. Запрос возвращает правильный код ответа (409)
    7. При создании с существующим логином возвращается ошибка
    ''')
    def test_create_duplicate_courier_error(self, generate_courier_data_and_cleanup):
        first_response = requests.post(CREATE_COURIER_URL, json=generate_courier_data_and_cleanup)
        assert first_response.status_code == 201

        duplicate_response = requests.post(CREATE_COURIER_URL, json=generate_courier_data_and_cleanup)
        assert duplicate_response.status_code == 409
        assert duplicate_response.json() == {
            "code": 409,
            "message": "Этот логин уже используется. Попробуйте другой."
        }


    @allure.title('Ошибка при отсутствии обязательных полей')
    @allure.description('''
    Покрываем требования:
    3. Для создания нужны все обязательные поля (login, password)
    4. Запрос возвращает правильный код ответа (400)
    6. При отсутствии полей возвращается ошибка
    ''')
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_create_courier_missing_field_error(self, generate_courier_data_and_cleanup, missing_field):
        payload = generate_courier_data_and_cleanup.copy()
        payload.pop(missing_field)

        response = requests.post(CREATE_COURIER_URL, json=payload)

        assert response.status_code == 400
        assert "Недостаточно данных для создания учетной записи" in response.json().get("message")
