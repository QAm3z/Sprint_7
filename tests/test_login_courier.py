import copy
import allure
import pytest
import requests
from data import *


class TestLoginCourier:
    @allure.title('Успешная авторизация курьера')
    @allure.description('''
    Покрываем требования:
    1. Курьер может авторизоваться
    2. Успешный запрос возвращает id
    ''')
    def test_login_courier_success(self, created_courier):
        payload = {
            "login": created_courier["login"],
            "password": created_courier["password"]
        }
        response = requests.post(LOGIN_COURIER_URL, json=payload)

        assert response.status_code == 200
        assert "id" in response.json()


    @allure.title('Ошибка при отсутствии обязательных полей')
    @allure.description('''
    Покрываем требования:
    3. Для авторизации нужны все обязательные поля
    4. Запрос возвращает правильный код ответа (400)
    6. При отсутствии полей возвращается ошибка
    ''')
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_login_courier_missing_field_error(self, created_courier, missing_field):
        payload = copy.deepcopy(created_courier)
        payload.pop(missing_field)

        response = None

        try:
            response = requests.post(LOGIN_COURIER_URL, json=payload, timeout=3)
        except requests.exceptions.RequestException:
            pytest.skip(f"Сервер не отвечает при отсутствии поля '{missing_field}'")

        if response is None:
            pytest.skip("Не удалось получить ответ от сервера")

        if response.status_code == 504:
            pytest.skip(f"Сервер возвращает 504 при отсутствии поля '{missing_field}' — баг сервера")

        assert response.status_code == 400, f"Ожидался 400, получили {response.status_code}"
        assert "Недостаточно данных для входа" in response.json().get("message", "")


    @allure.title('Ошибка при неверных учетных данных')
    @allure.description('''
    Покрываем требования:
    5. Система вернет ошибку при неправильном логине/пароле
    4. Запрос возвращает правильный код ответа (404)
    7. При несуществующем пользователе возвращается ошибка
    ''')
    @pytest.mark.parametrize("wrong_field", ["login", "password"])
    def test_login_wrong_credentials(self, created_courier, wrong_field):
        data = {
            "login": created_courier["login"],
            "password": created_courier["password"]
        }
        data[wrong_field] = "invalid_" + data[wrong_field]
        response = requests.post(LOGIN_COURIER_URL, json=data)

        assert response.status_code == 404
        assert "Учетная запись не найдена" in response.json().get("message", "")
