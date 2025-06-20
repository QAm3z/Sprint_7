import string
import random

import pytest
from data import *
import requests


@pytest.fixture
def generate_courier_data_and_cleanup():
    letters = string.ascii_lowercase
    random_string = ''.join(random.choice(letters) for i in range(10))
    payload = {
        "login": random_string,
        "password": random_string,
        "firstName": random_string
    }

    yield payload

    login_response = requests.post(
        LOGIN_COURIER_URL,
        json={
            "login": payload["login"],
            "password": payload["password"]
        }
    )
    if login_response.status_code == 200:
        courier_id = login_response.json()["id"]
        requests.delete(f'{DELETE_COURIER_URL}{courier_id}')


@pytest.fixture
def created_courier(generate_courier_data_and_cleanup):
    response = requests.post(CREATE_COURIER_URL, json=generate_courier_data_and_cleanup)
    if response.status_code == 201:
        return generate_courier_data_and_cleanup


@pytest.fixture
def generate_order_data():
    letters = string.ascii_lowercase
    random_string = ''.join(random.choice(letters) for i in range(10))
    return {
        'firstName': random_string,
        'lastName': random_string,
        'address': random_string,
        'metroStation': 1,
        'phone': '+7999' + ''.join(random.choice(string.digits) for _ in range(7)),
        'rentTime': 1,  # Только один раз
        'deliveryDate': '2023-12-31',
        'comment': random_string,
        'color': []  # Пустой массив по умолчанию
    }
