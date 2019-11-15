import requests
from time import time
from json import JSONDecodeError
from typing import Optional, Union

from .errors import ComagicException, ComagicParamsError
from .models import (Account, VirtualNumber, AvailableVirtualNumber, SipLine, Scenario, MediaField, Campaign,
                     CampaignAvailablePhoneNumber, CampaignAvailableRedirectPhoneNumber, )


class Comagic(object):
    def __init__(self, login: str = "", password: str = "", token: str = "", uis: bool = False) -> None:
        """
        :param login: str (login from comagic account)
        :param password: str (password from comagic account)
        :param token: str (token from comagic if needed.)
        :param uis: bool (if you wanna use uis api)
        """
        self._comagic_ap_id = None
        if uis:
            api_url = "https://dataapi.uiscom.ru/v2.0"
        else:
            api_url = "https://dataapi.comagic.ru/v2.0"
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
        if 'data' in resp['result']:
            return resp["result"]["data"]
        return resp['result']

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

    def get_account(self, user_id: Optional[int] = None):
        params = self._create_endpoint_params('get', 'account', user_id=user_id)
        response = self._send_api_request(params)
        return Account.from_dict(response)

    def get_virtual_numbers(self, limit: Optional[int] = None, offset: Optional[int] = None,
                            filter: dict = {}, fields: list = [], sort: list = [],
                            user_id: Optional[int] = None) -> any:
        if not fields:
            fields = VirtualNumber.fields()
        params = self._create_endpoint_params('get', 'virtual_numbers', user_id=user_id,
                                              limit=limit, offset=offset, filter=filter,
                                              fields=fields, sort=sort)
        response = self._send_api_request(params)
        return map(VirtualNumber.from_dict, response)

    def get_available_virtual_numbers(self, limit: Optional[int] = None, offset: Optional[int] = None,
                                      filter: dict = {}, fields: list = [], sort: list = [],
                                      user_id: Optional[int] = None) -> Union[map, ComagicException]:
        if not fields:
            fields = AvailableVirtualNumber.fields()
        params = self._create_endpoint_params('get', 'available_virtual_numbers', user_id=user_id,
                                              limit=limit, offset=offset, filter=filter,
                                              fields=fields, sort=sort)
        response = self._send_api_request(params)
        return map(AvailableVirtualNumber.from_dict, response)

    def enable_virtual_number(self, virtual_phone_number: str, user_id: Optional[int] = None) -> dict:
        params = self._create_endpoint_params('enable', 'virtual_numbers', user_id=user_id,
                                              virtual_phone_number=virtual_phone_number)
        return self._send_api_request(params)

    def disable_virtual_number(self, virtual_phone_number: str,
                               user_id: Optional[int] = None) -> Union[dict, ComagicException]:
        params = self._create_endpoint_params('disable', 'virtual_numbers', user_id=user_id,
                                              virtual_phone_number=virtual_phone_number)
        return self._send_api_request(params)

    def get_sip_line_virtual_numbers(self, limit: Optional[int] = None, offset: Optional[int] = None,
                                     filter: dict = {}, fields: list = [], sort: list = [],
                                     user_id: Optional[int] = None) -> Union[dict, ComagicException]:
        params = self._create_endpoint_params('get', 'sip_line_virtual_numbers', user_id=user_id,
                                              limit=limit, offset=offset, filter=filter,
                                              fields=fields, sort=sort)
        return self._send_api_request(params)

    def create_sip_line(self, employee_id: int, virtual_phone_number: str, user_id: Optional[int] = None) -> any:
        params = self._create_endpoint_params('create', 'sip_lines', user_id=user_id, employee_id=employee_id,
                                              virtual_phone_number=virtual_phone_number)
        response = self._send_api_request(params)
        return SipLine.from_dict(response)

    def update_sip_line(self, id: int, employee_id: int, virtual_phone_number: str, billing_state: Optional[str],
                        channels_count: Optional[int] = None, user_id: Optional[int] = None) -> any:
        if billing_state is not None and billing_state not in ('active', 'manual_lock'):
            raise ComagicParamsError('billing_state not in [active, manual_lock]')
        params = self._create_endpoint_params('update', 'sip_lines', id=id, employee_id=employee_id,
                                              virtual_phone_number=virtual_phone_number, billing_state=billing_state,
                                              channels_count=channels_count, user_id=user_id)
        return self._send_api_request(params)

    def delete_sip_line(self, id: int, user_id: Optional[int] = None) -> any:
        params = self._create_endpoint_params('delete', 'sip_lines', user_id=user_id, id=id)
        return self._send_api_request(params)

    def get_sip_lines(self, limit: Optional[int] = None, offset: Optional[int] = None,
                      filter: dict = {}, fields: list = [], sort: list = [],
                      user_id: Optional[int] = None) -> Union[map, ComagicException]:
        params = self._create_endpoint_params('get', 'sip_lines', user_id=user_id,
                                              limit=limit, offset=offset, filter=filter,
                                              fields=fields, sort=sort)
        response = self._send_api_request(params)
        return map(SipLine.from_dict, response)

    def update_sip_line_password(self, id: int, user_id: Optional[int] = None) -> Union[dict, ComagicException]:
        params = self._create_endpoint_params('update', 'sip_line_password', user_id=user_id, id=id)
        return self._send_api_request(params)

    def get_scenarios(self, limit: Optional[int] = None, offset: Optional[int] = None,
                      filter: dict = {}, fields: list = [], sort: list = [],
                      user_id: Optional[int] = None) -> Union[map, ComagicException]:
        params = self._create_endpoint_params('get', 'scenarios', user_id=user_id,
                                              limit=limit, offset=offset, filter=filter,
                                              fields=fields, sort=sort)
        response = self._send_api_request(params)
        return map(Scenario.from_dict, response)

    def get_media_files(self, limit: Optional[int] = None, offset: Optional[int] = None,
                        filter: dict = {}, fields: list = [], sort: list = [],
                        user_id: Optional[int] = None) -> Union[map, ComagicException]:
        params = self._create_endpoint_params('get', 'media_files', user_id=user_id,
                                              limit=limit, offset=offset, filter=filter,
                                              fields=fields, sort=sort)
        response = self._send_api_request(params)
        return map(MediaField.from_dict, response)

    def get_campaigns(self, limit: Optional[int] = None, offset: Optional[int] = None,
                      filter: dict = {}, fields: list = [], sort: list = [],
                      user_id: Optional[int] = None) -> Union[map, ComagicException]:
        if not fields:
            fields = Campaign.fields()
        params = self._create_endpoint_params('get', 'campaigns', user_id=user_id,
                                              limit=limit, offset=offset, filter=filter,
                                              fields=fields, sort=sort)
        response = self._send_api_request(params)
        return map(Campaign.from_dict, response)

    def delete_campaign(self, id: int, user_id: Optional[int] = None) -> Union[dict, ComagicException]:
        params = self._create_endpoint_params('delete', 'campaigns', user_id=user_id, id=id)
        return self._send_api_request(params)

    def get_campaign_available_phone_numbers(self, limit: Optional[int] = None, offset: Optional[int] = None,
                                             filter: dict = {}, fields: list = [], sort: list = [],
                                             user_id: Optional[int] = None) -> Union[map, ComagicException]:
        if not fields:
            fields = CampaignAvailablePhoneNumber.fields()
        params = self._create_endpoint_params('get', 'campaign_available_phone_numbers', user_id=user_id,
                                              limit=limit, offset=offset, filter=filter,
                                              fields=fields, sort=sort)
        response = self._send_api_request(params)
        return map(CampaignAvailablePhoneNumber.from_dict, response)

    def get_campaign_available_redirection_phone_numbers(self, limit: Optional[int] = None,
                                                         offset: Optional[int] = None,
                                                         filter: dict = {}, fields: list = [], sort: list = [],
                                                         user_id: Optional[int] = None) -> Union[map, ComagicException]:
        if not fields:
            fields = CampaignAvailableRedirectPhoneNumber.fields()
        params = self._create_endpoint_params('get', 'campaign_available_redirection_phone_numbers', user_id=user_id,
                                              limit=limit, offset=offset, filter=filter,
                                              fields=fields, sort=sort)
        response = self._send_api_request(params)
        return map(CampaignAvailableRedirectPhoneNumber.from_dict, response)

