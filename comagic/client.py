import requests
from time import time
from json import JSONDecodeError


class Comagic(object):
    def __init__(self, login: str = "", password: str = "", token: str = "", uis: bool = False) -> None:
        """
        :param login: str (login from comagic account)
        :param password: str (password from comagic account)
        :param token: str (token from comagic if needed.)
        :param uis: bool (if you wanna use uis api)
        """
        self._comagic_ap_id = None
        if (login and password) or token:
            self.login = login
            self.password = password
            self.API_URL = api_url
            self._session = requests.Session()
            self._session.headers.update({"Content-Type": "application/json"})
            self.access_token = self._create_access_token() if not token else token
        else:
            raise ValueError("miss auth params login and password or token")

    def _send_api_request(self, params: dict) -> any:
        """
        :param params: dict (params for comagic request)
        :param counter: int
        :return: any (data or raise ComagicException)
        """
        try:
            resp = self._session.post(self.API_URL, json=params).json()
        except (JSONDecodeError, requests.ConnectionError) as e:
            raise ComagicException({"code": 502, "message": f"{e}"})
        if "error" in resp:
            if resp["error"]["code"] == -32001:
                return self._send_api_request(params)
            raise ComagicException(resp["error"])
        return resp["result"]["data"]

    def _create_access_token(self) -> str:
        params = {
            "jsonrpc": "2.0",
            "id": f"req_call{int(time())}",
            "method": "login.user",
            "params": {"login": self.login, "password": self.password},
        }

        resp = self._send_api_request(params)
        self._comagic_app_id = resp["app_id"]
        return resp["access_token"]

    def _create_endpoint_params(self, method: str, endpoint: str, user_id: any = None, **kwargs) -> dict:
        """
        :param method: str
        :param endpoint: str
        :param user_id: any (int or None)
        :param date_form: str
        :param date_to: str
        :return: any
        """
        default_params = {
            "jsonrpc": "2.0",
            "id": f"req_{method}_{endpoint}_{time()}",
            "method": f"{method}.{endpoint}",
            "params": {"access_token": self.access_token},
        }
        if user_id:
            default_params["params"].update({"user_id": user_id})
        if kwargs:
            params = {key: value for key, value in kwargs.items() if value or isinstance(value, (bool, int))}
            default_params["params"].update(**params)
        # print(default_params)
        return default_params
