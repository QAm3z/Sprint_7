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
        with allure.step("Подготовить валидные учетные данные"):
            payload = {
                "login": created_courier["login"],
                "password": created_courier["password"]
            }

        with allure.step("Отправить запрос на авторизацию"):
            response = requests.post(LOGIN_COURIER_URL, json=payload)

        with allure.step("Проверить успешную авторизацию"):
            assert response.status_code == HTTP_200
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
        with allure.step("Подготовить данные без обязательного поля"):
            payload = {
                "login": created_courier["login"],
                "password": created_courier["password"]
            }
            payload.pop(missing_field)

        with allure.step("Отправить запрос с неполными данными"):
            response = requests.post(LOGIN_COURIER_URL, json=payload)

        with allure.step("Проверить ошибку валидации"):
            assert response.status_code == HTTP_400, f"Ожидался {HTTP_400}, получили {response.status_code}"
            assert MISSING_FIELD_LOGIN_RESPONSE["message"] in response.json().get("message", "")


    @allure.title('Ошибка при неверных учетных данных')
    @allure.description('''
    Покрываем требования:
    5. Система вернет ошибку при неправильном логине/пароле
    4. Запрос возвращает правильный код ответа (404)
    7. При несуществующем пользователе возвращается ошибка
    ''')
    @pytest.mark.parametrize("wrong_field", ["login", "password"])
    def test_login_wrong_credentials(self, created_courier, wrong_field):
        with allure.step("Подготовить неверные учетные данные"):
            data = {
                "login": created_courier["login"],
                "password": created_courier["password"]
            }
            data[wrong_field] = "invalid_" + data[wrong_field]

        with allure.step("Отправить запрос с неверными данными"):
            response = requests.post(LOGIN_COURIER_URL, json=data)

        with allure.step("Проверить ошибку авторизации"):
            assert response.status_code == HTTP_404
            assert ACCOUNT_NOT_FOUND_RESPONSE["message"] in response.json().get("message", "")
