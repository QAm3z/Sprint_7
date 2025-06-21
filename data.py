BASE_URL = 'https://qa-scooter.praktikum-services.ru'
CREATE_COURIER_URL = f'{BASE_URL}/api/v1/courier'
LOGIN_COURIER_URL = f'{BASE_URL}/api/v1/courier/login'
DELETE_COURIER_URL = f'{BASE_URL}/api/v1/courier/'
CREATE_ORDER_URL = f'{BASE_URL}/api/v1/orders'
GET_ORDERS_URL = f'{BASE_URL}/api/v1/orders'

HTTP_200 = 200
HTTP_201 = 201
HTTP_400 = 400
HTTP_404 = 404
HTTP_409 = 409
HTTP_504 = 504

SUCCESS_CREATION_RESPONSE = {"ok": True}
DUPLICATE_LOGIN_RESPONSE = {
    "code": 409,
    "message": "Этот логин уже используется. Попробуйте другой."
}
MISSING_FIELD_RESPONSE = {
    "message": "Недостаточно данных для создания учетной записи"
}
MISSING_FIELD_LOGIN_RESPONSE = {
    "message": "Недостаточно данных для входа"
}
ACCOUNT_NOT_FOUND_RESPONSE = {
    "message": "Учетная запись не найдена"
}
SUCCESS_ORDER_RESPONSE_KEYS = ["track"]