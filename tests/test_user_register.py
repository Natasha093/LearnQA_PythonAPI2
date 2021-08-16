import pytest
import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions


class TestUserRegister(BaseCase):
    def test_create_user_successfully(self):
        data = self.prepare_registration_data()

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)
        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode(
            "utf-8") == f"Users with email '{email}' already exists", f"Unexpected content {response.content}"

    def test_create_user_without_req_symbol(self):
        email = 'userexample.com'
        data = {
            'password': '1234',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': email
        }

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Invalid email format"

    incomplete_dataset = ((
                              {'username': 'learnqa',
                               'firstName': 'learnqa',
                               'lastName': 'learnqa',
                               'email': 'user@example.com'
                               }, "password"),
                          ({'password': '123',
                            'firstName': 'learnqa',
                            'lastName': 'learnqa',
                            'email': 'user@example.com'
                            }, "username"),
                          ({'password': '123',
                            'username': 'learnqa',
                            'lastName': 'learnqa',
                            'email': 'user@example.com'
                            }, "firstName"),
                          ({'password': '123',
                            'username': 'learnqa',
                            'firstName': 'learnqa',
                            'email': 'user@example.com'
                            }, "lastName"),
                          ({'password': '123',
                            'username': 'learnqa',
                            'firstName': 'learnqa',
                            'lastName': 'learnqa'
                            }, "email")
    )

    @pytest.mark.parametrize("data, answer", incomplete_dataset)
    def test_create_user_without_any_req_field(self, data, answer):
        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The following required params are missed: {answer}"

    def test_create_user_with_one_symbol_username(self):

        data = {
            'password': '1234',
            'username': 'learnqa',
            'firstName': 'a',
            'lastName': 'learnqa',
            'email': self.email
        }
        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The value of 'firstName' field is too short"

    def test_create_user_with_very_long_username(self):
        data = {
            'password': '1234',
            'username': 'learnqa',
            'firstName': 'a' * 251,
            'lastName': 'learnqa',
            'email': self.email
        }
        response = requests.post("https://playground.learnqa.ru/api/user", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The value of 'firstName' field is too long"
