from .utils import parse_datetime


class BaseModel(object):
    def __init__(self, **kwargs) -> None:
        fields = self.fields()
        self.__set_default_attrs()
        for field, value in kwargs.items():
            if field not in fields:
                print("Invalid field - ", field)
                raise AttributeError('%s not in attributes for this %s' % field, self.__class__.__name__)
            setattr(self, field, value)

    def __set_default_attrs(self) -> None:
        for field in self.fields():
            setattr(self, field, None)

    @classmethod
    def from_dict(cls, model_dict):
        raise NotImplemented

    @classmethod
    def fields(cls) -> list:
        raise NotImplemented

    def to_dict(self) -> dict:
        return {field: getattr(self, field) for field in self.fields() if getattr(self, field)}

    def __repr__(self):
        state = ['%s=%s' % (k, repr(v)) for (k, v) in vars(self).items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(state))

    def __getitem__(self, item):
        return self.__dict__[item]

    def keys(self):
        return self.__dict__.keys()

    def values(self):
        return self.__dict__.values()

    def items(self):
        return self.__dict__.items()

    def pop(self, *args):
        return self.__dict__.pop(*args)

    def __iter__(self):
        return iter(self.__dict__)

    def __contains__(self, item):
        return item in self.__dict__

    def __delitem__(self, key):
        del self.__dict__[key]

    def __setitem__(self, key, item):
        self.__dict__[key] = item


class Account(BaseModel):
    @classmethod
    def fields(cls) -> list:
        return ['app_id', 'name', 'timezone']

    @classmethod
    def from_dict(cls, model_dict):
        return cls(**model_dict)


class VirtualNumber(BaseModel):
    @classmethod
    def fields(cls) -> list:
        return [
            'id', 'virtual_phone_number', 'redirection_phone_number',
            'activation_date', 'status', 'category', 'type', 'campaigns',
            'site_blocks', 'scenarios'
        ]

    @classmethod
    def from_dict(cls, model_dict):
        model_dict['activation_data'] = parse_datetime(model_dict.get('activation_data'))
        return cls(**model_dict)


class SipLine(BaseModel):
    @classmethod
    def fields(cls) -> list:
        return [
            'id', 'phone_number', 'type', 'employee_id', 'employee_full_name',
            'channels_count', 'dial_time', 'billing_state', 'physical_state',
            'status', 'virtual_phone_number', 'ip_addresses', 'password', 'server',
        ]

    @classmethod
    def from_dict(cls, model_dict):
        return cls(**model_dict)


class Scenario(BaseModel):
    @classmethod
    def fields(cls) -> list:
        return [
            'id', 'name', 'virtual_phone_numbers', 'sites', 'campaigns'
        ]

    @classmethod
    def from_dict(cls, model_dict):
        return cls(**model_dict)


class MediaField(BaseModel):
    @classmethod
    def fields(cls) -> list:
        return [
            'id', 'name', 'duration', 'play_link', 'normalization', 'size', 'type'
        ]

    @classmethod
    def from_dict(cls, model_dict):
        return cls(**model_dict)


class Campaign(BaseModel):
    @classmethod
    def fields(cls) -> list:
        return [
            'id', 'name', 'description', 'status', 'creation_time', 'engine', 'type', 'costs',
            'cost_ratio', 'cost_ratio_operator', 'site_id', 'site_domain_name', 'site_blocks',
            'dynamic_call_tracking', 'campaign_conditions'
        ]

    @classmethod
    def from_dict(cls, model_dict):
        model_dict = parse_datetime(model_dict.get('creation_time'))
        return cls(**model_dict)


class Site(BaseModel):
    @classmethod
    def fields(cls) -> list:
        return [
            'id', 'domain_name', 'default_phone_number', 'default_scenario', 'site_key', 'industry_id', 'creation_date',
            'industry_name', 'target_call_min_duration', 'track_subdomains', 'cookie_lifetime', 'campaign_lifetime',
            'sales_enabled', 'second_communication_period', 'services_enabled', 'replacement_dynamical_block_enabled',
            'widget_link', 'show_visitor_id', 'site_blocks', 'connected_integrations'
        ]

    @classmethod
    def from_dict(cls, model_dict):
        model_dict['creation_date'] = parse_datetime(model_dict.get('creation_date'))
        return cls(**model_dict)


class Tag(BaseModel):
    @classmethod
    def fields(cls) -> list:
        return [
            'id', 'name', 'is_system'
        ]

    @classmethod
    def from_dict(cls, model_dict):
        return cls(**model_dict)


class Employee(BaseModel):
    @classmethod
    def fields(cls) -> list:
        return [
            'id', 'first_name', 'last_name', 'patronymic', 'full_name', 'status', 'allowed_in_call_types',
            'allowed_out_call_types', 'email', 'call_recording', 'calls_available', 'schedule_id', 'schedule_name',
            'coach', 'phone_numbers', 'extension', 'operator'
        ]

    @classmethod
    def from_dict(cls, model_dict):
        return cls(**model_dict)


class Contact(BaseModel):
    @classmethod
    def fields(cls) -> list:
        return [
            'id', 'last_name', 'first_name', 'patronymic', 'full_name', 'emails',
            'groups', 'phone_numbers', 'personal_manager_id', 'personal_manager_full_name',
            'organization_name', 'organization_id'
        ]

    @classmethod
    def from_dict(cls, model_dict):
        return cls(**model_dict)


class Schedule(BaseModel):
    @classmethod
    def fields(cls) -> list:
        return [
            'id', 'name', 'schedules'
        ]

    @classmethod
    def from_dict(cls, model_dict):
        return cls(**model_dict)


class CampaignDailyStat(BaseModel):
    @classmethod
    def fields(cls) -> list:
        return [
            'date', 'site_id', 'site_domain_name', 'campain_id', 'campaign_name', 'campaign_ext_id',
            'campaign_ext_name', 'engine', 'banner_group_id', 'banner_group_name', 'keyword_id', 'keyword',
            'banner_id', 'banner_name', 'old_banner_ids', 'cost_sum', 'shows_count', 'clicks_count', 'calls_count',
            'chats_count', 'goals_count', 'offline_messages_count', 'session_ids', 'daily_budget', 'communications',
        ]

    @classmethod
    def from_dict(cls, model_dict):
        model_dict['date'] = parse_datetime(model_dict.get('date'))
        return cls(**model_dict)


class Customer(BaseModel):
    @classmethod
    def fields(cls) -> list:
        return [
            'id', 'name', 'description', 'creation_date', 'status_change_date_time', 'tariff_plan_id',
            'tariff_plan_name', 'monthly_base_limit', 'monthly_base_notify_limit', 'monthly_base_notify_emails',
            'monthly_calls_limit', 'monthly_calls_notify_limit', 'monthly_calls_notify_emails', 'daily_calls_limit',
            'daily_calls_notify_limit', 'daily_calls_notify_emails', 'sites'
        ]

    @classmethod
    def from_dict(cls, model_dict):
        model_dict['creation_date'] = parse_datetime(model_dict.get('creation_date'))
        return cls(**model_dict)


class Communication(BaseModel):
    @classmethod
    def fields(cls) -> list:
        return [
            'id', 'communication_type', 'communication_number', 'communication_page_url', 'date_time',
            'ua_client_id', 'ym_client_id', 'sale_date', 'sale_cost', 'search_query', 'search_engine',
            'referrer_domain', 'referrer', 'entrance_page', 'gclid', 'yclid', 'ymclid', 'ef_id', 'channel',
            'tags', 'site_id', 'site_domain_name', 'campaign_id', 'campaign_name', 'visit_other_campaign',
            'visitor_id', 'person_id', 'visitor_type', 'visitor_session_id', 'visits_count',
            'visitor_first_campaign_id', 'visitor_first_campaign_name', 'visitor_city', 'visitor_region',
            'visitor_country', 'visitor_device', 'visitor_custom_properties', 'segments', 'utm_source', 'utm_medium',
            'utm_term', 'utm_content', 'utm_campaign', 'openstat_ad', 'openstat_campaign', 'openstat_service',
            'openstat_source', 'eq_utm_source', 'eq_utm_medium', 'eq_utm_term', 'eq_utm_content', 'eq_utm_campaign',
            'eq_utm_referrer', 'eq_utm_expid', 'attributes'
        ]

    @classmethod
    def from_dict(cls, model_dict):
        model_dict['date_time'] = parse_datetime(model_dict.get('date_time'))
        model_dict['sale_date'] = parse_datetime(model_dict.get('sale_date'))
        return cls(**model_dict)


class Call(BaseModel):
    @classmethod
    def fields(cls) -> list:
        return [
            'id', 'start_time', 'finish_time', 'finish_reason', 'direction', 'cpn_region_id', 'cpn_region_name',
            'scenario_operations', 'is_lost', 'communication_number', 'communication_page_url', 'contact_phone_number',
            'communication_id', 'communication_type', 'wait_duration', 'total_wait_duration',
            'lost_call_processing_duration', 'talk_duration', 'clean_talk_duration', 'total_duration',
            'postprocess_duration', 'call_records', 'virtual_phone_number', 'ua_client_id', 'ym_client_id',
            'sale_date', 'sale_cost', 'is_transfer', 'search_query', 'search_engine', 'referrer_domain', 'referrer',
            'entrance_page', 'gclid', 'yclid', 'ymclid', 'ef_id', 'channel', 'tags', 'employees',
            'last_answered_employee_id', 'last_answered_employee_full_name', 'last_answered_employee_rating',
            'first_answered_employee_id', 'first_answered_employee_full_name', 'scenario_id', 'scenario_name',
            'site_domain_name', 'site_id', 'campaign_name', 'campaign_id', 'visit_other_campaign', 'visitor_id',
            'person_id', 'visitor_type', 'visitor_session_id', 'visits_count', 'visitor_first_campaign_id',
            'visitor_first_campaign_name', 'visitor_city', 'visitor_region', 'visitor_country', 'visitor_device',
            'visitor_custom_properties', 'segments', 'contact_id', 'contact_full_name', 'utm_source', 'utm_medium',
            'utm_term', 'utm_content', 'utm_campaign', 'openstat_ad', 'openstat_campaign', 'openstat_service',
            'openstat_source', 'attributes', 'eq_utm_source', 'eq_utm_medium', 'eq_utm_term', 'eq_utm_content',
            'eq_utm_campaign', 'eq_utm_referrer', 'eq_utm_expid', 'utm_referrer', 'source',
        ]

    @classmethod
    def from_dict(cls, model_dict):
        model_dict['start_time'] = parse_datetime(model_dict.get('start_time'))
        model_dict['finish_time'] = parse_datetime(model_dict.get('finish_time'))
        model_dict['sale_date'] = parse_datetime(model_dict.get('sale_date'))
        return cls(**model_dict)


class CallLegs(BaseModel):
    @classmethod
    def fields(cls) -> list:
        return [
            'id', 'call_session_id', 'call_records', 'start_time', 'connect_time', 'duration', 'total_duration',
            'virtual_phone_number', 'calling_phone_number', 'called_phone_number', 'direction', 'is_transfered',
            'is_operator', 'employee_id', 'employee_full_name', 'employee_phone_number', 'employee_rating',
            'scenario_id', 'scenario_name', 'is_coach', 'release_cause_code', 'release_cause_description',
            'is_failed', 'is_talked', 'contact_id', 'contact_full_name', 'contact_phone_number', 'action_id',
            'action_name', 'group_id', 'group_name'
        ]

    @classmethod
    def from_dict(cls, model_dict):
        model_dict['start_time'] = parse_datetime(model_dict.get('start_time'))
        model_dict['connect_time'] = parse_datetime(model_dict.get('connect_time'))
        return cls(**model_dict)


class Goal(BaseModel):
    @classmethod
    def fields(cls) -> list:
        return [
            'id', 'date_time', 'name', 'type', 'ext_id', 'source', 'communication_number', 'communication_page_url',
            'communication_id', 'communication_type', 'ua_client_id', 'ym_client_id', 'sale_date', 'sale_cost',
            'search_query', 'search_engine', 'referrer_domain', 'referrer', 'entrance_page', 'gclid', 'yclid', 'ymclid',
            'ef_id', 'channel', 'tags', 'site_id', 'site_domain_name', 'campaign_id', 'campaign_name',
            'visit_other_campaign', 'visitor_id', 'person_id', 'visitor_type', 'visitor_session_id', 'visits_count',
            'visitor_first_campaign_id', 'visitor_first_campaign_name', 'visitor_city', 'visitor_region',
            'visitor_country', 'visitor_device', 'visitor_custom_properties', 'segments', 'utm_source', 'utm_medium',
            'utm_term', 'utm_content', 'utm_campaign', 'openstat_ad', 'openstat_campaign', 'openstat_service',
            'openstat_source', 'eq_utm_source', 'eq_utm_medium', 'eq_utm_term', 'eq_utm_content', 'eq_utm_campaign',
            'eq_utm_referrer', 'eq_utm_expid', 'attributes', 'utm_referrer',
        ]

    @classmethod
    def from_dict(cls, model_dict):
        model_dict['date_time'] = parse_datetime(model_dict.get('date_time'))
        model_dict['sale_date'] = parse_datetime(model_dict.get('sale_date'))
        return cls(**model_dict)


class Chat(BaseModel):
    @classmethod
    def fields(cls) -> list:
        return [
            'id', 'status', 'initiator', 'date_time', 'duration', 'answer_time', 'communication_number',
            'communication_page_url', 'communication_id', 'communication_type', 'messages_count', 'ua_client_id',
            'ym_client_id', 'sale_date', 'sale_cost', 'is_transfer', 'release_cause', 'search_query',
            'search_engine', 'referrer_domain', 'referrer', 'entrance_page', 'gclid', 'yclid', 'ymclid', 'ef_id',
            'channel', 'employee_id', 'employee_full_name', 'employee_messages_count', 'employee_raiting', 'site_id',
            'site_domain_name', 'campaign_id', 'campaign_name', 'visit_other_campaign', 'visitor_id', 'person_id',
            'visitor_type', 'visitor_session_id', 'visits_count', 'visitor_first_campaign_id',
            'visitor_first_campaign_name', 'visitor_city', 'visitor_region', 'visitor_country', 'visitor_device',
            'utm_source', 'utm_medium', 'utm_term', 'utm_content', 'utm_campaign', 'openstat_ad',
            'openstat_campaign', 'openstat_service', 'openstat_source', 'eq_utm_source', 'eq_utm_medium',
            'eq_utm_term', 'eq_utm_content', 'eq_utm_campaign', 'eq_utm_referrer', 'eq_utm_expid', 'attributes',
            'visitor_custom_properties', 'segments', 'tags', 'utm_referrer', 'source',
        ]

    @classmethod
    def from_dict(cls, model_dict):
        model_dict['date_time'] = parse_datetime(model_dict.get('date_time'))
        model_dict['sale_date'] = parse_datetime(model_dict.get('sale_date'))
        return cls(**model_dict)


class ChatMessage(BaseModel):
    @classmethod
    def fields(cls) -> list:
        return [
            'chat_id', 'date_time', 'text', 'source', 'employee_id', 'employee_full_name'
        ]

    @classmethod
    def from_dict(cls, model_dict):
        model_dict['date_time'] = parse_datetime(model_dict.get('model_dict'))
        return cls(**model_dict)


class OfflineMessage(BaseModel):
    @classmethod
    def fields(cls) -> list:
        return [
            'id', 'date_time', 'text', 'communication_number', 'communication_page_url', 'communication_type',
            'communication_id', 'ua_client_id', 'ym_client_id', 'sale_date', 'sale_cost', 'status', 'process_time',
            'form_type', 'search_query', 'search_engine', 'referrer_domain', 'referrer', 'entrance_page', 'gclid',
            'yclid', 'ymclid', 'ef_id', 'channel', 'group_id', 'group_name', 'employee_id', 'employee_full_name',
            'employee_answer_message', 'employee_comment', 'tags', 'site_id', 'site_domain_name', 'campaign_id',
            'campaign_name', 'visit_other_campaign', 'visitor_phone_number', 'visitor_email', 'visitor_name',
            'visitor_id', 'person_id', 'visitor_type', 'visitor_session_id', 'visitor_first_campaign_id',
            'visitor_first_campaign_id', 'visitor_first_campaign_name', 'visitor_city', 'visitor_country',
            'visitor_region', 'visitor_device', 'visitor_custom_properties', 'segments', 'utm_source', 'utm_medium',
            'utm_term', 'utm_content', 'utm_campaign', 'openstat_ad', 'openstat_campaign', 'openstat_service',
            'openstat_source', 'attributes', 'eq_utm_source', 'eq_utm_medium', 'eq_utm_term', 'eq_utm_content',
            'eq_utm_campaign', 'eq_utm_referrer', 'eq_utm_expid', 'utm_referrer', 'source',
        ]

    @classmethod
    def from_dict(cls, model_dict):
        model_dict['date_time'] = parse_datetime(model_dict.get('date_time'))
        model_dict['sale_date'] = parse_datetime(model_dict.get('sale_date'))
        model_dict['process_time'] = parse_datetime(model_dict.get('process_time'))
        return cls(**model_dict)


class VisitorSession(BaseModel):
    @classmethod
    def fields(cls) -> list:
        return [
            'date_time', 'id', 'ua_client_id', 'ym_client_id', 'gclid', 'yclid', 'ef_id', 'ymclid', 'cm_id',
            'integrated_campaign_data', 'referrer_domain', 'referrer', 'search_engine', 'search_query',
            'entrance_page', 'exit_page', 'duration', 'channel', 'engine', 'campaign_id', 'campaign_name', 'site_id',
            'site_domain_name', 'person_id', 'visitor_id', 'visitor_device', 'visitor_country', 'visitor_city',
            'visitor_region', 'visitor_ip_address', 'visitor_type', 'visitor_browser_name',
            'visitor_browser_version', 'visitor_os_name', 'visitor_os_version', 'visitor_provider', 'visitor_screen',
            'visitor_language', 'visitor_custom_properties', 'utm_source', 'utm_medium', 'utm_term', 'utm_content',
            'utm_campaign', 'openstat_ad', 'openstat_campaign', 'openstat_service', 'openstat_source', 'hits_count',
            'hits', 'hit_time', 'hit_duration', 'hit_url', 'segments', 'segment_name', 'segment_id', 'communications',
        ]

    @classmethod
    def from_dict(cls, model_dict):
        model_dict['date_time'] = parse_datetime(model_dict.get('date_time'))
        return cls(**model_dict)


class FinancialCallLegs(BaseModel):
    @classmethod
    def fields(cls) -> list:
        return [
            'start_time', 'direction', 'source', 'call_session_id', 'leg_id', 'calling_phone_number',
            'called_phone_number', 'duration', 'chargeable_duration', 'direction_type', 'cost_per_minute',
            'total_charge', 'bonuses_charge',
        ]

    @classmethod
    def from_dict(cls, model_dict):
        model_dict['start_time'] = parse_datetime(model_dict.get('start_time'))
        super().from_dict(model_dict)


class AvailableVirtualNumber(BaseModel):
    @classmethod
    def fields(cls) -> list:
        return [
            'phone_number', 'category', 'location_mnemonic', 'location_name', 'onetime_payment', 'monthly_charge',
            'min_charge',
        ]


class CampaignAvailablePhoneNumber(BaseModel):
    @classmethod
    def fields(cls) -> list:
        return [
            'id', 'phone_number', 'type'
        ]

    @classmethod
    def from_dict(cls, model_dict):
        return cls(**model_dict)


class CampaignAvailableRedirectPhoneNumber(BaseModel):
    @classmethod
    def fields(cls) -> list:
        return [
            'id', 'phone_number',
        ]

    @classmethod
    def from_dict(cls, model_dict):
        return cls(**model_dict)


class CampaignWeight(BaseModel):
    @classmethod
    def fields(cls) -> list:
        return [
            'site_id', 'site_domain_name', 'entrance_page', 'referrer_domain', 'search_engine', 'search_query',
            'engine', 'referrer', 'channel', 'location', 'utm_tags', 'os_tags', 'other_tags',
        ]

    @classmethod
    def from_dict(cls, model_dict):
        return cls(**model_dict)


class SiteBlock(BaseModel):
    @classmethod
    def fields(cls) -> list:
        return [
            'id', 'name', 'site_id', 'site_domain_name', 'templates', 'phone_numbers'
        ]

    @classmethod
    def from_dict(cls, model_dict):
        return cls(**model_dict)


class EmployeeGroup(BaseModel):
    @classmethod
    def fields(cls) -> list:
        return [
            'id', 'name', 'members', 'phone_number', 'group_phone_number', 'queue_enabled', 'channels_count'
        ]

    @classmethod
    def from_dict(cls, model_dict):
        return cls(**model_dict)


class CustomerUser(BaseModel):
    @classmethod
    def fields(cls) -> list:
        return [
            'id', 'name', 'description', 'login', 'customer_id'
        ]

    @classmethod
    def from_dict(cls, model_dict):
        return cls(**model_dict)


class ContactGroup(BaseModel):
    @classmethod
    def fields(cls) -> list:
        return [
            'id', 'name', 'is_system', 'members'
        ]

    @classmethod
    def from_dict(cls, model_dict):
        return cls(**model_dict)


class ContactOrganization(BaseModel):
    @classmethod
    def fields(cls) -> list:
        return [
            'id', 'name',
        ]

    @classmethod
    def from_dict(cls, model_dict):
        return cls(**model_dict)
