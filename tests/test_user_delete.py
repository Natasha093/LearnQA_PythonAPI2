import time
from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.my_requests import MyRequests


class TestUserDelete(BaseCase):
    def test_to_delete_user_id_2(self):
        # LOGIN
        login_data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response_login = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(response_login, "auth_sid")
        token = self.get_header(response_login, "x-csrf-token")

        # DELETE
        response_del = MyRequests.delete("/user/2", headers={'x-csrf-token': token},
                                         cookies={'auth_sid': auth_sid})
        Assertions.assert_code_status(response_del, 400)
        assert response_del.content.decode('utf-8') == 'Please, do not delete test users with ID 1, 2, 3, 4 or 5.'

    def test_delete_new_user(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response_create = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response_create, 200)
        Assertions.assert_json_has_key(response_create, "id")

        email = register_data['email']
        password = register_data['password']
        user_id = self.get_json_value(response_create, "id")

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        response_login = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response_login, "auth_sid")
        token = self.get_header(response_login, "x-csrf-token")

        # DELETE
        response_del = MyRequests.delete("/user/2", headers={'x-csrf-token': token},
                                         cookies={'auth_sid': auth_sid})

        Assertions.assert_code_status(response_del, 200)

        # GET
        response_get = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
        )
        Assertions.assert_code_status(response_get, 404)
        assert response_get.content.decode('utf-8') == 'User not found'

    def test_delete_other_user(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response_create = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response_create, 200)
        Assertions.assert_json_has_key(response_create, "id")

        email = register_data['email']
        password = register_data['password']
        user_id = self.get_json_value(response_create, "id")

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        response_login = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response_login, "auth_sid")
        token = self.get_header(response_login, "x-csrf-token")

        # REGISTER OTHER
        time.sleep(1)
        register_data = self.prepare_registration_data()
        response_create_other = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response_create_other, 200)
        Assertions.assert_json_has_key(response_create_other, "id")

        email_other = register_data['email']
        password_other = register_data['password']
        user_id_other = self.get_json_value(response_create_other, "id")

        # LOGIN OTHER
        login_data_other = {
            'email': email_other,
            'password': password_other
        }
        response_login_other = MyRequests.post("/user/login", data=login_data_other)

        auth_sid_other = self.get_cookie(response_login_other, "auth_sid")
        token_other = self.get_header(response_login_other, "x-csrf-token")

        # DELETE
        response_del = MyRequests.delete(f"/user/{user_id_other}", headers={'x-csrf-token': token},
                                         cookies={'auth_sid': auth_sid})
        Assertions.assert_code_status(response_del, 200)

        # GET OTHER
        response_get = MyRequests.get(
            f"/user/{user_id_other}",
            headers={"x-csrf-token": token_other},
            cookies={"auth_sid": auth_sid_other},
        )
        Assertions.assert_code_status(response_get, 200)
        Assertions.assert_json_value_by_name(
            response_get,
            "id",
            user_id_other,
            "User not found"
        )
