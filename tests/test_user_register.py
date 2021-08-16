import allure
import pytest
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


@allure.epic("Create user")
class TestUserRegister(BaseCase):
    @allure.title("Create user successfully")
    def test_create_user_successfully(self):
        data = self.prepare_registration_data()

        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    @allure.title("Create user with existing email")
    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode(
            "utf-8") == f"Users with email '{email}' already exists", f"Unexpected content {response.content}"

    @allure.title("Create user without @ in email")
    def test_create_user_without_req_symbol(self):
        email = 'userexample.com'
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user/", data=data)
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

    @allure.title("Create user without param: {answer}")
    @pytest.mark.parametrize("data, answer", incomplete_dataset)
    def test_create_user_without_any_req_field(self, data, answer):
        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The following required params are missed: {answer}"

    @allure.title("Create user with one symbol in username")
    def test_create_user_with_one_symbol_username(self):
        data = self.prepare_registration_data()
        email = data.get("email")
        data = {
            'password': '1234',
            'username': 'learnqa',
            'firstName': 'a',
            'lastName': 'learnqa',
            'email': email
        }
        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The value of 'firstName' field is too short"

    @allure.title("Create user with too long username")
    @allure.description("This test checks code and answer if username > 250 symbols")
    def test_create_user_with_very_long_username(self):
        data = self.prepare_registration_data()
        email = data.get("email")
        data = {
            'password': '1234',
            'username': 'learnqa',
            'firstName': 'a' * 251,
            'lastName': 'learnqa',
            'email': email
        }
        response = MyRequests.post("/user", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The value of 'firstName' field is too long"
