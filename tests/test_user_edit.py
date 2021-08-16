from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


class TestUserEdit(BaseCase):
    def test_edit_just_created_user(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT
        new_name = "Changed Name"

        response3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_name}
        )

        Assertions.assert_code_status(response3, 200)

        # GET
        response4 = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
        )

        Assertions.assert_json_value_by_name(
            response4,
            "firstName",
            new_name,
            "Wrong name of the user after edit"
        )

    def test_edit_user_not_auth(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        user_id = self.get_json_value(response1, "id")

        # EDIT
        new_name = "Changed Name"

        response3 = MyRequests.put(
            f"/user/{user_id}",
            data={"firstName": new_name}
        )
        Assertions.assert_code_status(response3, 400)
        assert response3.content.decode("utf-8") == f"Auth token not supplied"

    def test_edit_other_user(self):
        # REGISTER USER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        password = register_data['password']

        # LOGIN USER
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # REGISTER OTHER USER
        register_data = self.prepare_registration_data()
        response3 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response3, 200)
        Assertions.assert_json_has_key(response3, "id")

        other_email = register_data['email']
        other_first_name = register_data['firstName']
        other_password = register_data['password']
        other_user_id = self.get_json_value(response3, "id")

        # LOGIN OTHER USER
        other_login_data = {
            'email': other_email,
            'password': other_password
        }
        response4 = MyRequests.post("/user/login", data=other_login_data)

        other_auth_sid = self.get_cookie(response4, "auth_sid")
        other_token = self.get_header(response4, "x-csrf-token")

        # EDIT OTHER USER
        new_name = "Changed Name"

        response5 = MyRequests.put(
                f"/user/{other_user_id}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid},
                data={"firstName": new_name}
            )

        Assertions.assert_code_status(response5, 200)

        # GET OTHER USER
        response7 = MyRequests.get(
                f"/user/{other_user_id}",
                headers={"x-csrf-token": other_token},
                cookies={"auth_sid": other_auth_sid},
            )

        Assertions.assert_json_value_by_name(
                response7,
                "firstName",
                other_first_name,
                "Name was changed for other user"
            )

    def test_edit_user_invalid_email(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT
        new_email = 'userexample.com'

        response3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"email": new_email}
        )

        Assertions.assert_code_status(response3, 400)
        assert response3.content.decode("utf-8") == f"Invalid email format"

    def test_edit_user_short_firstname(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT
        new_name = "a"

        response3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_name}
        )

        Assertions.assert_code_status(response3, 400)
        Assertions.assert_json_value_by_name(
            response3,
            "error",
            "Too short value for field firstName",
            "Wrong error"
        )
