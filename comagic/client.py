import requests
from time import time
from datetime import datetime
from json import JSONDecodeError
from typing import Optional, Union

from .errors import ComagicException, ComagicParamsError
from .utils import DATETIME_FORMAT
from .models import (Account, VirtualNumber, AvailableVirtualNumber, SipLine, Scenario, MediaField, Campaign,
                     CampaignAvailablePhoneNumber, CampaignAvailableRedirectPhoneNumber, CampaignWeight, Site,
                     SiteBlock, Tag, Employee, EmployeeGroup, CustomerUser, Call, CallLegs, FinancialCallLegs,
                     Customer, Communication, Contact, Chat, ChatMessage, Schedule, VisitorSession, OfflineMessage,
                     Goal, ContactGroup, ContactOrganization, CampaignDailyStat)


class Comagic(object):
    def __init__(self, login: str = "", password: str = "", token: str = "", uis: bool = False) -> None:
        """
        :param login: str (login from comagic account)
        :param password: str (password from comagic account)
        :param token: str (token from comagic if needed.)
        :param uis: bool (if you wanna use uis api)
        """
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

    def _send_api_request(self, params: dict, auth_counter=0) -> any:
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
            if resp["error"]["code"] == -32001 and auth_counter <= 3:
                return self._send_api_request(params, auth_counter + 1)
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
            params = {key: value for key, value in kwargs.items() if value is not None}
            default_params["params"].update(**params)
        # print(default_params)
        return default_params

    def get_account(self, user_id: Optional[int] = None):
        params = self._create_endpoint_params('get', 'account', user_id=user_id)
        response = self._send_api_request(params)
        return Account.from_dict(response[0])

    def get_virtual_numbers(self, limit: Optional[int] = None, offset: Optional[int] = None,
                            filter: dict = None, fields: list = None, sort: list = None,
                            user_id: Optional[int] = None) -> any:
        if not fields:
            fields = VirtualNumber.fields()
        kwargs = {
            'limit': limit,
            'offset': offset,
            'filter': filter,
            'fields': fields,
            'sort': sort,
        }
        params = self._create_endpoint_params('get', 'virtual_numbers', user_id=user_id, **kwargs)
        response = self._send_api_request(params)
        return map(VirtualNumber.from_dict, response)

    def get_available_virtual_numbers(self, limit: Optional[int] = None, offset: Optional[int] = None,
                                      filter: dict = None, fields: list = None, sort: list = None,
                                      user_id: Optional[int] = None) -> Union[map, ComagicException]:
        if not fields:
            fields = AvailableVirtualNumber.fields()
        kwargs = {
            'limit': limit,
            'offset': offset,
            'filter': filter,
            'fields': fields,
            'sort': sort,
        }
        params = self._create_endpoint_params('get', 'available_virtual_numbers', user_id=user_id, **kwargs)
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
                                     filter: dict = None, fields: list = None, sort: list = None,
                                     user_id: Optional[int] = None) -> any:
        kwargs = {
            'limit': limit,
            'offset': offset,
            'filter': filter,
            'fields': fields,
            'sort': sort,
        }
        params = self._create_endpoint_params('get', 'sip_line_virtual_numbers', user_id=user_id, **kwargs)
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
        kwargs = {
            'virtual_phone_number': virtual_phone_number,
            'billing_state': billing_state,
            'channels_count': channels_count,
            'id': id,
            'employee_id': employee_id
        }
        params = self._create_endpoint_params('update', 'sip_lines', user_id=user_id, **kwargs)
        return self._send_api_request(params)

    def delete_sip_line(self, id: int, user_id: Optional[int] = None) -> any:
        params = self._create_endpoint_params('delete', 'sip_lines', user_id=user_id, id=id)
        return self._send_api_request(params)

    def get_sip_lines(self, limit: Optional[int] = None, offset: Optional[int] = None,
                      filter: dict = None, fields: list = None, sort: list = None,
                      user_id: Optional[int] = None) -> any:
        kwargs = {
            'limit': limit,
            'offset': offset,
            'filter': filter,
            'fields': fields,
            'sort': sort,
        }
        params = self._create_endpoint_params('get', 'sip_lines', user_id=user_id, **kwargs)
        response = self._send_api_request(params)
        return map(SipLine.from_dict, response)

    def update_sip_line_password(self, id: int, user_id: Optional[int] = None) -> Union[dict, ComagicException]:
        params = self._create_endpoint_params('update', 'sip_line_password', user_id=user_id, id=id)
        return self._send_api_request(params)

    def get_scenarios(self, limit: Optional[int] = None, offset: Optional[int] = None,
                      filter: dict = None, fields: list = None, sort: list = None,
                      user_id: Optional[int] = None) -> any:
        if not fields:
            fields = Scenario.fields()
        kwargs = {
            'limit': limit,
            'offset': offset,
            'filter': filter,
            'fields': fields,
            'sort': sort,
        }
        params = self._create_endpoint_params('get', 'scenarios', user_id=user_id, **kwargs)
        response = self._send_api_request(params)
        return map(Scenario.from_dict, response)

    def get_media_files(self, limit: Optional[int] = None, offset: Optional[int] = None,
                        filter: dict = None, fields: list = None, sort: list = None,
                        user_id: Optional[int] = None) -> any:
        if not fields:
            fields = MediaField.fields()
        kwargs = {
            'limit': limit,
            'offset': offset,
            'filter': filter,
            'fields': fields,
            'sort': sort,
        }
        params = self._create_endpoint_params('get', 'media_files', user_id=user_id, **kwargs)
        response = self._send_api_request(params)
        return map(MediaField.from_dict, response)

    def get_campaigns(self, limit: Optional[int] = None, offset: Optional[int] = None,
                      filter: dict = None, fields: list = None, sort: list = None,
                      user_id: Optional[int] = None) -> any:
        if not fields:
            fields = Campaign.fields()
        kwargs = {
            'limit': limit,
            'offset': offset,
            'filter': filter,
            'fields': fields,
            'sort': sort,
        }
        params = self._create_endpoint_params('get', 'campaigns', user_id=user_id, **kwargs)
        response = self._send_api_request(params)
        return map(Campaign.from_dict, response)

    def delete_campaign(self, id: int, user_id: Optional[int] = None) -> Union[dict, ComagicException]:
        params = self._create_endpoint_params('delete', 'campaigns', user_id=user_id, id=id)
        return self._send_api_request(params)

    def get_campaign_available_phone_numbers(self, limit: Optional[int] = None, offset: Optional[int] = None,
                                             filter: dict = None, fields: list = None, sort: list = None,
                                             user_id: Optional[int] = None) -> any:
        if not fields:
            fields = CampaignAvailablePhoneNumber.fields()
        kwargs = {
            'limit': limit,
            'offset': offset,
            'filter': filter,
            'fields': fields,
            'sort': sort,
        }
        params = self._create_endpoint_params('get', 'campaign_available_phone_numbers', user_id=user_id, **kwargs)
        response = self._send_api_request(params)
        return map(CampaignAvailablePhoneNumber.from_dict, response)

    def get_campaign_available_redirection_phone_numbers(self, limit: Optional[int] = None,
                                                         offset: Optional[int] = None,
                                                         filter: dict = None, fields: list = None, sort: list = None,
                                                         user_id: Optional[int] = None) -> any:
        if not fields:
            fields = CampaignAvailableRedirectPhoneNumber.fields()
        kwargs = {
            'limit': limit,
            'offset': offset,
            'filter': filter,
            'fields': fields,
            'sort': sort,
        }
        params = self._create_endpoint_params('get', 'campaign_available_redirection_phone_numbers', user_id=user_id,
                                              **kwargs)
        response = self._send_api_request(params)
        return map(CampaignAvailableRedirectPhoneNumber.from_dict, response)

    def create_campaign(self, name: str, status: str, site_id: int, site_blocks: list,
                        campaign_conditions: list, dynamic_call_tracking: list,
                        description: Optional[str] = None, user_id: Optional[int] = None) -> any:
        kwargs = {
            'name': name,
            'status': status,
            'site_id': site_id,
            'site_blocks': site_blocks,
            'campaign_conditions': campaign_conditions,
            'dynamic_call_tracking': dynamic_call_tracking,
            'description': description,
        }
        params = self._create_endpoint_params('create', 'campaign', user_id=user_id, **kwargs)
        return self._send_api_request(params)

    def update_campaign(self, id: int, name: str, status: str, site_id: int, site_blocks: list,
                        campaign_conditions: list, dynamic_call_tracking: list,
                        description: Optional[str] = None, user_id: Optional[int] = None) -> any:
        kwargs = {
            'name': name,
            'status': status,
            'site_id': site_id,
            'site_blocks': site_blocks,
            'campaign_conditions': campaign_conditions,
            'dynamic_call_tracking': dynamic_call_tracking,
            'description': description,
            'id': id,
        }
        params = self._create_endpoint_params('create', 'campaign', user_id=user_id, **kwargs)
        return self._send_api_request(params)

    def get_campaign_parameter_weights(self, limit: Optional[int] = None,
                                       offset: Optional[int] = None,
                                       filter: dict = None, fields: list = None, sort: list = None,
                                       user_id: Optional[int] = None) -> any:
        if not fields:
            fields = CampaignWeight.fields()
        kwargs = {
            'limit': limit,
            'offset': offset,
            'filter': filter,
            'fields': fields,
            'sort': sort,
        }
        params = self._create_endpoint_params('get', 'campaign_parameter_weights', user_id=user_id, **kwargs)
        response = self._send_api_request(params)
        return CampaignWeight.from_dict(response)

    def update_campaign_parameter_weights(self, site_id: int, entrance_page: Optional[int] = None,
                                          referrer_domain: Optional[int] = None, search_engine: Optional[int] = None,
                                          search_query: Optional[int] = None, engine: Optional[int] = None,
                                          referrer: Optional[int] = None, channel: Optional[int] = None,
                                          location: Optional[int] = None, utm_tags: Optional[int] = None,
                                          os_tags: Optional[int] = None, other_tags: Optional[int] = None,
                                          user_id=None) -> any:
        kwargs = {
            'entrance_page': entrance_page,
            'site_id': site_id,
            'referrer_domain': referrer_domain,
            'search_engine': search_engine,
            'search_query': search_query,
            'engine': engine,
            'referrer': referrer,
            'channel': channel,
            'location': location,
            'utm_tags': utm_tags,
            'os_tags': os_tags,
            'other_tags': other_tags,
        }
        params = self._create_endpoint_params('update', 'campaign_parameter_weights', user_id=user_id, **kwargs)
        return self._send_api_request(params)

    def create_site(self, domain_name: str, default_phone_number: str, industry_id: int,
                    target_call_min_duration: Optional[int] = None, track_subdomains_enabled: Optional[bool] = None,
                    default_scenario_id: Optional[int] = None, cookie_lifetime: Optional[int] = None,
                    campaign_lifetime: Optional[int] = None, sales_enabled: Optional[bool] = None,
                    second_communication_period: Optional[int] = None, services_enabled: Optional[bool] = None,
                    replacement_dynamical_block_enabled: Optional[bool] = None, widget_link: Optional[dict] = None,
                    show_visitor_id: Optional[dict] = None, user_id: Optional[int] = None) -> dict:
        kwargs = {
            'domain_name': domain_name,
            'default_phone_number': default_phone_number,
            'industry_id': industry_id,
            'target_call_min_duration': target_call_min_duration,
            'track_subdomains_enabled': track_subdomains_enabled,
            'default_scenario_id': default_scenario_id,
            'cookie_lifetime': cookie_lifetime,
            'campaign_lifetime': campaign_lifetime,
            'sales_enabled': sales_enabled,
            'second_communication_period': second_communication_period,
            'services_enabled': services_enabled,
            'replacement_dynamical_block_enabled': replacement_dynamical_block_enabled,
            'widget_link': widget_link,
            'show_visitor_id': show_visitor_id,
        }
        params = self._create_endpoint_params('create', 'sites', user_id=user_id, **kwargs)
        return self._send_api_request(params)

    def update_site(self, id: int, domain_name: str, default_phone_number: str, industry_id: int,
                    target_call_min_duration: Optional[int] = None, track_subdomains_enabled: Optional[bool] = None,
                    default_scenario_id: Optional[int] = None, cookie_lifetime: Optional[int] = None,
                    campaign_lifetime: Optional[int] = None, sales_enabled: Optional[bool] = None,
                    second_communication_period: Optional[int] = None, services_enabled: Optional[bool] = None,
                    replacement_dynamical_block_enabled: Optional[bool] = None, widget_link: Optional[dict] = None,
                    show_visitor_id: Optional[dict] = None, user_id: Optional[int] = None) -> dict:
        kwargs = {
            'domain_name': domain_name,
            'default_phone_number': default_phone_number,
            'industry_id': industry_id,
            'target_call_min_duration': target_call_min_duration,
            'track_subdomains_enabled': track_subdomains_enabled,
            'default_scenario_id': default_scenario_id,
            'cookie_lifetime': cookie_lifetime,
            'campaign_lifetime': campaign_lifetime,
            'sales_enabled': sales_enabled,
            'second_communication_period': second_communication_period,
            'services_enabled': services_enabled,
            'replacement_dynamical_block_enabled': replacement_dynamical_block_enabled,
            'widget_link': widget_link,
            'show_visitor_id': show_visitor_id,
            'id': id,
        }
        params = self._create_endpoint_params('update', 'sites', user_id=user_id, **kwargs)
        return self._send_api_request(params)

    def delete_site(self, id: int, user_id: Optional[int] = None) -> dict:
        kwargs = {
            'id': id
        }
        params = self._create_endpoint_params('delete', 'sites', user_id=user_id, **kwargs)
        return self._send_api_request(params)

    def get_sites(self, limit: Optional[int] = None,
                  offset: Optional[int] = None,
                  filter: dict = None, fields: list = None, sort: list = None,
                  user_id: Optional[int] = None) -> any:
        kwargs = {
            'limit': limit,
            'offset': offset,
            'filter': filter,
            'fields': fields,
            'sort': sort,
        }
        params = self._create_endpoint_params('get', 'sites', user_id=user_id, **kwargs)
        response = self._send_api_request(params)
        return map(Site.from_dict, response)

    def create_site_blocks(self, site_id: int, name: str, user_id: Optional[int] = None) -> dict:
        kwargs = {
            'site_od': site_id,
            'name': name
        }
        params = self._create_endpoint_params('create', 'site_blocks', user_id=user_id, **kwargs)
        return self._send_api_request(params)

    def get_site_blocks(self, limit: Optional[int] = None,
                        offset: Optional[int] = None,
                        filter: dict = None, fields: list = None, sort: list = None,
                        user_id: Optional[int] = None) -> any:
        if not fields:
            fields = SiteBlock.fields()
        kwargs = {
            'limit': limit,
            'offset': offset,
            'filter': filter,
            'fields': fields,
            'sort': sort,
        }
        params = self._create_endpoint_params('get', 'site_blocks', user_id=user_id, **kwargs)
        response = self._send_api_request(params)
        return map(SiteBlock.from_dict, response)

    def delete_site_block(self, id: int, user_id: Optional[int] = None) -> dict:
        params = self._create_endpoint_params('delete', 'site_blocks', user_id=user_id, id=id)
        return self._send_api_request(params)

    def update_site_block(self, id: int, name: str, user_id: Optional[int] = None) -> dict:
        kwargs = {
            'id': id,
            'name': name
        }
        params = self._create_endpoint_params('update', 'site_blocks', user_id=user_id, **kwargs)
        return self._send_api_request(params)

    def create_tag(self, name: str, user_id: Optional[int] = None) -> dict:
        params = self._create_endpoint_params('create', 'tags', user_id=user_id, name=name)
        return self._send_api_request(params)

    def update_tag(self, id: int, name: str, user_id: Optional[int] = None) -> dict:
        params = self._create_endpoint_params('update', 'tags', user_id=user_id, id=id, name=name)
        return self._send_api_request(params)

    def delete_tag(self, id: int, user_id: Optional[int] = None) -> dict:
        params = self._create_endpoint_params('delete', 'tags', user_id=user_id, id=id)
        return self._send_api_request(params)

    def get_tags(self, limit: Optional[int] = None,
                 offset: Optional[int] = None,
                 filter: dict = None, fields: list = None, sort: list = None,
                 user_id: Optional[int] = None) -> any:
        if not fields:
            fields = Tag.fields()
        kwargs = {
            'limit': limit,
            'offset': offset,
            'filter': filter,
            'fields': fields,
            'sort': sort,
        }
        params = self._create_endpoint_params('get', 'tags', user_id=user_id, **kwargs)
        response = self._send_api_request(params)
        return map(Tag.from_dict, response)

    def get_employees(self, limit: Optional[int] = None,
                      offset: Optional[int] = None,
                      filter: dict = None, fields: list = None, sort: list = None,
                      user_id: Optional[int] = None) -> any:
        if not fields:
            fields = Employee.fields()
        kwargs = {
            'limit': limit,
            'offset': offset,
            'filter': filter,
            'fields': fields,
            'sort': sort,
        }
        params = self._create_endpoint_params('get', 'employees', user_id=user_id, **kwargs)
        response = self._send_api_request(params)
        return map(Employee.from_dict, response)

    def create_employee(self, last_name: str, phone_numbers: list, first_name: Optional[str] = None,
                        patronymic: Optional[str] = None,
                        status: Optional[str] = None, allowed_in_call_types: Optional[list] = None,
                        allowed_out_call_types: Optional[list] = None, email: Optional[str] = None,
                        call_recording: Optional[str] = None, schedule_id: Optional[int] = None,
                        calls_available: Optional[bool] = None, extension: Optional[dict] = None,
                        operator: Optional[dict] = None, user_id: Optional[int] = None) -> dict:
        if status is not None \
                and status not in ('available', 'break', 'do_not_disturb',
                                   'not_at_workplace', 'not_at_work', 'unknown'):
            raise ComagicParamsError('invalid status, status must be in [available, break, do_not_disturb, '
                                     'not_at_workplace, not_at_work, unknown]')
        if call_recording is not None \
                and call_recording not in ('all', 'in', 'out', 'off'):
            raise ComagicParamsError('invalid call_recording, call_recording must be in [all, in, out, off]')
        kwargs = {
            'last_name': last_name,
            'phone_numbers': phone_numbers,
            'first_name': first_name,
            'patronymic': patronymic,
            'allowed_in_call_types': allowed_in_call_types,
            'allowed_out_call_types': allowed_out_call_types,
            'email': email,
            'call_recording': call_recording,
            'status': status,
            'schedule_id': schedule_id,
            'calls_available': calls_available,
            'extension': extension,
            'operator': operator,
        }
        params = self._create_endpoint_params('create', 'employees', user_id=user_id, **kwargs)
        return self._send_api_request(params)

    def delete_employee(self, id: int, user_id: Optional[int] = None) -> dict:
        params = self._create_endpoint_params('delete', 'employee', user_id=user_id, id=id)
        return self._send_api_request(params)

    def update_employee(self, id: int, last_name: Optional[str] = None, phone_numbers: Optional[list] = None,
                        first_name: Optional[str] = None,
                        patronymic: Optional[str] = None,
                        status: Optional[str] = None, allowed_in_call_types: Optional[list] = None,
                        allowed_out_call_types: Optional[list] = None, email: Optional[str] = None,
                        call_recording: Optional[str] = None, schedule_id: Optional[int] = None,
                        calls_available: Optional[bool] = None, extension: Optional[dict] = None,
                        operator: Optional[dict] = None, user_id: Optional[int] = None) -> dict:
        if status is not None \
                and status not in ('available', 'break', 'do_not_disturb',
                                   'not_at_workplace', 'not_at_work', 'unknown'):
            raise ComagicParamsError('invalid status, status must be in [available, break, do_not_disturb, '
                                     'not_at_workplace, not_at_work, unknown]')
        if call_recording is not None \
                and call_recording not in ('all', 'in', 'out', 'off'):
            raise ComagicParamsError('invalid call_recording, call_recording must be in [all, in, out, off]')
        kwargs = {
            'last_name': last_name,
            'id': id,
            'phone_numbers': phone_numbers,
            'first_name': first_name,
            'patronymic': patronymic,
            'allowed_in_call_types': allowed_in_call_types,
            'allowed_out_call_types': allowed_out_call_types,
            'email': email,
            'call_recording': call_recording,
            'status': status,
            'schedule_id': schedule_id,
            'calls_available': calls_available,
            'extension': extension,
            'operator': operator,
        }
        params = self._create_endpoint_params('update', 'employees', user_id=user_id, **kwargs)
        return self._send_api_request(params)

    def create_employees_group(self, name: str, members: Optional[list] = None,
                               group_phone_number: Optional[str] = None,
                               queue_enabled: Optional[bool] = None,
                               channels_count: Optional[int] = None,
                               user_id: Optional[int] = None) -> dict:
        kwargs = {
            'name': name,
            'members': members,
            'group_phone_number': group_phone_number,
            'queue_enabled': queue_enabled,
            'channels_count': channels_count,
        }
        params = self._create_endpoint_params('create', 'group_employees', user_id=user_id, **kwargs)
        return self._send_api_request(params)

    def delete_employees_group(self, id: int, user_id: Optional[int] = None) -> dict:
        params = self._create_endpoint_params('delete', 'group_employees', user_id=user_id, id=id)
        return self._send_api_request(params)

    def update_employees_group(self, id: int, name: Optional[str] = None, members: Optional[list] = None,
                               group_phone_number: Optional[str] = None,
                               queue_enabled: Optional[bool] = None,
                               channels_count: Optional[int] = None,
                               user_id: Optional[int] = None) -> dict:
        kwargs = {
            'name': name,
            'id': id,
            'members': members,
            'group_phone_number': group_phone_number,
            'queue_enabled': queue_enabled,
            'channels_count': channels_count,
        }
        params = self._create_endpoint_params('update', 'group_employees', user_id=user_id, **kwargs)
        return self._send_api_request(params)

    def get_employees_groups(self, limit: Optional[int] = None,
                             offset: Optional[int] = None,
                             filter: dict = None, fields: list = None, sort: list = None,
                             user_id: Optional[int] = None) -> any:
        if not fields:
            fields = EmployeeGroup.fields()
        kwargs = {
            'limit': limit,
            'offset': offset,
            'filter': filter,
            'fields': fields,
            'sort': sort,
        }
        params = self._create_endpoint_params('get', 'group_employees', user_id=user_id, **kwargs)
        response = self._send_api_request(params)
        return map(EmployeeGroup.from_dict, response)

    def get_customer_users(self, limit: Optional[int] = None,
                           offset: Optional[int] = None,
                           filter: dict = None, fields: list = None, sort: list = None,
                           user_id: Optional[int] = None) -> any:
        if not fields:
            fields = CustomerUser.fields()
        kwargs = {
            'limit': limit,
            'offset': offset,
            'filter': filter,
            'fields': fields,
            'sort': sort,
        }
        params = self._create_endpoint_params('get', 'customer_users', user_id=user_id, **kwargs)
        response = self._send_api_request(params)
        return map(CustomerUser.from_dict, response)

    def get_communication_report(self, date_from: datetime, date_till: datetime, limit: Optional[int] = None,
                                 offset: Optional[int] = None,
                                 filter: dict = None, fields: list = None, sort: list = None,
                                 user_id: Optional[int] = None) -> any:
        if not fields:
            fields = Communication.fields()
        kwargs = {
            'limit': limit,
            'offset': offset,
            'filter': filter,
            'fields': fields,
            'sort': sort,
            'date_from': date_from.strftime('%Y-%m-%d %H:%M:%S'),
            'date_till': date_till.strftime('%Y-%m-%d %H:%M:%S'),
        }
        params = self._create_endpoint_params('get', 'communications_report', user_id=user_id, **kwargs)
        response = self._send_api_request(params)
        return map(Communication.from_dict, response)

    def get_calls_report(self, date_from: datetime, date_till: datetime, limit: Optional[int] = None,
                         offset: Optional[int] = None,
                         filter: dict = None, fields: list = None, sort: list = None,
                         user_id: Optional[int] = None) -> any:
        if not fields:
            fields = Call.fields()
        kwargs = {
            'limit': limit,
            'offset': offset,
            'filter': filter,
            'fields': fields,
            'sort': sort,
            'date_from': date_from.strftime(DATETIME_FORMAT),
            'date_till': date_till.strftime(DATETIME_FORMAT),
        }
        params = self._create_endpoint_params('get', 'calls_report', user_id=user_id, **kwargs)
        response = self._send_api_request(params)
        return map(Call.from_dict, response)

    def get_call_legs_report(self, date_from: datetime, date_till: datetime, limit: Optional[int] = None,
                             offset: Optional[int] = None,
                             filter: dict = None, fields: list = None, sort: list = None,
                             user_id: Optional[int] = None) -> any:
        if not fields:
            fields = CallLegs.fields()
        kwargs = {
            'limit': limit,
            'offset': offset,
            'filter': filter,
            'fields': fields,
            'sort': sort,
            'date_from': date_from.strftime(DATETIME_FORMAT),
            'date_till': date_till.strftime(DATETIME_FORMAT),
        }
        params = self._create_endpoint_params('get', 'call_legs_report', user_id=user_id, **kwargs)
        response = self._send_api_request(params)
        return map(CallLegs.from_dict, response)

    def get_goals_report(self, date_from: datetime, date_till: datetime, limit: Optional[int] = None,
                         offset: Optional[int] = None,
                         filter: dict = None, fields: list = None, sort: list = None,
                         user_id: Optional[int] = None) -> any:
        if not fields:
            fields = Goal.fields()
        kwargs = {
            'limit': limit,
            'offset': offset,
            'filter': filter,
            'fields': fields,
            'sort': sort,
            'date_from': date_from.strftime(DATETIME_FORMAT),
            'date_till': date_till.strftime(DATETIME_FORMAT),
        }
        params = self._create_endpoint_params('get', 'goals_report', user_id=user_id, **kwargs)
        response = self._send_api_request(params)
        return map(Goal.from_dict, response)

    def get_chats_report(self, date_from: datetime, date_till: datetime, limit: Optional[int] = None,
                         offset: Optional[int] = None,
                         filter: dict = None, fields: list = None, sort: list = None,
                         user_id: Optional[int] = None) -> any:
        if not fields:
            fields = Chat.fields()
        kwargs = {
            'limit': limit,
            'offset': offset,
            'filter': filter,
            'fields': fields,
            'sort': sort,
            'date_from': date_from.strftime(DATETIME_FORMAT),
            'date_till': date_till.strftime(DATETIME_FORMAT),
        }
        params = self._create_endpoint_params('get', 'chats_report', user_id=user_id, **kwargs)
        response = self._send_api_request(params)
        return map(Chat.from_dict, response)

    def get_chat_messages_report(self, chat_id: int, limit: Optional[int] = None,
                                 offset: Optional[int] = None,
                                 filter: dict = None, fields: list = None, sort: list = None,
                                 user_id: Optional[int] = None) -> any:
        if not fields:
            fields = ChatMessage.fields()
        kwargs = {
            'limit': limit,
            'offset': offset,
            'filter': filter,
            'fields': fields,
            'sort': sort,
            'chat': chat_id
        }
        params = self._create_endpoint_params('get', 'chat_messages_report', user_id=user_id, **kwargs)
        response = self._send_api_request(params)
        return map(ChatMessage.from_dict, response)

    def get_offline_messages_report(self, date_from: datetime, date_till: datetime, limit: Optional[int] = None,
                                    offset: Optional[int] = None,
                                    filter: dict = None, fields: list = None, sort: list = None,
                                    user_id: Optional[int] = None) -> any:
        if not fields:
            fields = OfflineMessage.fields()
        kwargs = {
            'limit': limit,
            'offset': offset,
            'filter': filter,
            'fields': fields,
            'sort': sort,
            'date_from': date_from.strftime(DATETIME_FORMAT),
            'date_till': date_till.strftime(DATETIME_FORMAT),
        }
        params = self._create_endpoint_params('get', 'offline_messages_report', user_id=user_id, **kwargs)
        response = self._send_api_request(params)
        return map(OfflineMessage.from_dict, response)

    def get_visitor_sessions_report(self, date_from: datetime, date_till: datetime, limit: Optional[int] = None,
                                    offset: Optional[int] = None,
                                    filter: dict = None, fields: list = None, sort: list = None,
                                    user_id: Optional[int] = None) -> any:
        if not fields:
            fields = VisitorSession.fields()
        kwargs = {
            'limit': limit,
            'offset': offset,
            'filter': filter,
            'fields': fields,
            'sort': sort,
            'date_from': date_from.strftime(DATETIME_FORMAT),
            'date_till': date_till.strftime(DATETIME_FORMAT),
        }
        params = self._create_endpoint_params('get', 'visitor_sessions_report', user_id=user_id, **kwargs)
        response = self._send_api_request(params)
        return map(VisitorSession.from_dict, response)

    def get_financial_call_legs_report(self, date_from: datetime, date_till: datetime, limit: Optional[int] = None,
                                       offset: Optional[int] = None,
                                       filter: dict = None, fields: list = None, sort: list = None,
                                       user_id: Optional[int] = None) -> any:
        if not fields:
            fields = FinancialCallLegs.fields()
        kwargs = {
            'limit': limit,
            'offset': offset,
            'filter': filter,
            'fields': fields,
            'sort': sort,
            'date_from': date_from.strftime(DATETIME_FORMAT),
            'date_till': date_till.strftime(DATETIME_FORMAT),
        }
        params = self._create_endpoint_params('get', 'financial_call_legs_report', user_id=user_id, **kwargs)
        response = self._send_api_request(params)
        return map(FinancialCallLegs.from_dict, response)

    def get_contacts(self, limit: Optional[int] = None,
                     offset: Optional[int] = None,
                     filter: dict = None, fields: list = None, sort: list = None,
                     user_id: Optional[int] = None) -> any:
        if not fields:
            fields = Contact.fields()
        kwargs = {
            'limit': limit,
            'offset': offset,
            'filter': filter,
            'fields': fields,
            'sort': sort,
        }
        params = self._create_endpoint_params('get', 'contacts', user_id=user_id, **kwargs)
        response = self._send_api_request(params)
        return map(Contact.from_dict, response)

    def delete_contact(self, id: int, user_id: Optional[int] = None) -> any:
        params = self._create_endpoint_params('delete', 'contacts', user_id=user_id, id=id)
        return self._send_api_request(params)

    def create_contact(self, last_name: str, phone_numbers: list, first_name: Optional[str] = None,
                       patronymic: Optional[str] = None, emails: Optional[list] = None,
                       personal_manager_id: Optional[int] = None, organization_id: Optional[int] = None,
                       groups: Optional[list] = None, user_id: Optional[int] = None) -> dict:
        kwargs = {
            'last_name': last_name,
            'phone_numbers': phone_numbers,
            'first_name': first_name,
            'patronymic': patronymic,
            'emails': emails,
            'personal_manager_id': personal_manager_id,
            'organization_id': organization_id,
            'groups': groups,
        }
        params = self._create_endpoint_params('create', 'contacts', user_id=user_id, **kwargs)
        return self._send_api_request(params)

    def update_contact(self, id: int, last_name: str, phone_numbers: list, first_name: Optional[str] = None,
                       patronymic: Optional[str] = None, emails: Optional[list] = None,
                       personal_manager_id: Optional[int] = None, organization_id: Optional[int] = None,
                       groups: Optional[list] = None, user_id: Optional[int] = None) -> dict:
        kwargs = {
            'id': id,
            'last_name': last_name,
            'phone_numbers': phone_numbers,
            'first_name': first_name,
            'patronymic': patronymic,
            'emails': emails,
            'personal_manager_id': personal_manager_id,
            'organization_id': organization_id,
            'groups': groups,
        }
        params = self._create_endpoint_params('update', 'contacts', user_id=user_id, **kwargs)
        return self._send_api_request(params)

    def create_contact_group(self, name: str, members: Optional[list] = None, user_id: Optional[int] = None) -> dict:
        params = self._create_endpoint_params('create', 'group_contacts', user_id=user_id, name=name, members=members)
        return self._send_api_request(params)

    def delete_contact_group(self, id: int, user_id: Optional[int] = None) -> dict:
        params = self._create_endpoint_params('delete', 'group_contacts', user_id=user_id, id=id)
        return self._send_api_request(params)

    def update_contact_group(self, id: int, name: str, members: Optional[list] = None,
                             user_id: Optional[int] = None) -> dict:
        params = self._create_endpoint_params('update', 'group_contacts', user_id=user_id, name=name,
                                              members=members, id=id)
        return self._send_api_request(params)

    def get_contact_groups(self, limit: Optional[int] = None,
                           offset: Optional[int] = None,
                           filter: dict = None, fields: list = None, sort: list = None,
                           user_id: Optional[int] = None) -> any:
        if not fields:
            fields = ContactGroup.fields()
        kwargs = {
            'limit': limit,
            'offset': offset,
            'filter': filter,
            'fields': fields,
            'sort': sort,
        }
        params = self._create_endpoint_params('get', 'group_contacts', user_id=user_id, **kwargs)
        response = self._send_api_request(params)
        return map(ContactGroup.from_dict, response)

    def get_contact_organizations(self, limit: Optional[int] = None,
                                  offset: Optional[int] = None,
                                  filter: dict = None, fields: list = None, sort: list = None,
                                  user_id: Optional[int] = None) -> any:
        if not fields:
            fields = ContactOrganization.fields()
        kwargs = {
            'limit': limit,
            'offset': offset,
            'filter': filter,
            'fields': fields,
            'sort': sort,
        }
        params = self._create_endpoint_params('get', 'contact_organizations', user_id=user_id, **kwargs)
        response = self._send_api_request(params)
        return map(ContactOrganization.from_dict, response)

    def create_contact_organization(self, name: str, user_id: Optional[int] = None) -> dict:
        params = self._create_endpoint_params('create', 'contact_organizations', user_id=user_id, name=name)
        return self._send_api_request(params)

    def update_contact_organization(self, id: int, name: str, user_id: Optional[int] = None) -> dict:
        params = self._create_endpoint_params('update', 'contact_organizations', user_id=user_id, name=name, id=id)
        return self._send_api_request(params)

    def delete_contact_organization(self, id: int, user_id: Optional[int] = None) -> dict:
        params = self._create_endpoint_params('delete', 'contact_organizations', user_id=user_id, id=id)
        return self._send_api_request(params)

    def get_schedules(self, limit: Optional[int] = None,
                      offset: Optional[int] = None,
                      filter: dict = None, fields: list = None, sort: list = None,
                      user_id: Optional[int] = None) -> any:
        if not fields:
            fields = Schedule.fields()
        kwargs = {
            'limit': limit,
            'offset': offset,
            'filter': filter,
            'fields': fields,
            'sort': sort,
        }
        params = self._create_endpoint_params('get', 'schedules', user_id=user_id, **kwargs)
        response = self._send_api_request(params)
        return map(Schedule.from_dict, response)

    def create_schedule(self, name: str, schedules: Optional[list] = None, user_id: Optional[int] = None) -> dict:
        params = self._create_endpoint_params('create', 'schedules', user_id=user_id, name=name, schedules=schedules)
        return self._send_api_request(params)

    def delete_schedule(self, id: int, user_id: Optional[int] = None) -> dict:
        params = self._create_endpoint_params('delete', 'schedules', user_id=user_id, id=id)
        return self._send_api_request(params)

    def update_schedule(self, id: int, name: str, schedules: Optional[list] = None,
                        user_id: Optional[int] = None) -> dict:
        params = self._create_endpoint_params('update', 'schedules', user_id=user_id,
                                              id=id, name=name, schedules=schedules)
        return self._send_api_request(params)

    def get_campaign_daily_stat(self, date_from: datetime, date_till: datetime, limit: Optional[int] = None,
                                offset: Optional[int] = None,
                                filter: dict = None, fields: list = None, sort: list = None,
                                user_id: Optional[int] = None) -> any:
        if not fields:
            fields = CampaignDailyStat.fields()
        kwargs = {
            'limit': limit,
            'offset': offset,
            'filter': filter,
            'fields': fields,
            'sort': sort,
            'date_from': date_from.strftime(DATETIME_FORMAT),
            'date_till': date_till.strftime(DATETIME_FORMAT),
        }
        params = self._create_endpoint_params('get', 'campaign_daily_stat', user_id=user_id, **kwargs)
        response = self._send_api_request(params)
        return map(CampaignDailyStat.from_dict, response)

    def get_customers(self, limit: Optional[int] = None,
                      offset: Optional[int] = None,
                      filter: dict = None, fields: list = None, sort: list = None,
                      user_id: Optional[int] = None) -> any:
        if not fields:
            fields = Customer.fields()
        kwargs = {
            'limit': limit,
            'offset': offset,
            'filter': filter,
            'fields': fields,
            'sort': sort,
        }
        params = self._create_endpoint_params('get', 'customers', user_id=user_id, **kwargs)
        response = self._send_api_request(params)
        return map(Customer.from_dict, response)