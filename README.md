# Comagic-sdk for data api

# Installation

Install using `pip`...

    pip install comagic-data-api-sdk
    
# Usage
```python
from comagic import Comagic
client = Comagic("<login>", "<password>") # init comagic api
client = Comagic(token="<token>") # if u create access token in comagic interface

```
### Customers
doc - <a href='https://www.comagic.ru/support/api/data-api/Partners/'> Кленты агенства</a>
```python
customers = client.get_customer_users(limit=100, offset=0, fields=None, filter=None, sort=None)
```

### Sites
doc - <a href='https://www.comagic.ru/support/api/data-api/Sites/'>Сайт</a>

```python
sites = client.get_sites(limit=100, offset=0, fields=None, filter=None, sort=None, user_id='<user_id> if needed')

# create site
site = {
    'domain_name': 'test.ru',
    'default_phone_number': '79379992',
    'industry_id': 1,
}
client.create_site(**site, user_id='<user_id> if needed')

# delete site
client.delete_site(id='<site_id>', user_id='<user_id> if needed')

# update site
site = {
    'id': 1231,
    'domain_name': 'test1.ru',
    'default_phone_number': '79379992',
    'industry_id': 2,
}
client.update_site(**site, user_id='<user_id> if needed')

# create site blocks
client.create_site_blocks(site_id=123, name='test_site_block', user_id='<user_id> if needed')

# get site blocks
site_blocks = client.get_site_blocks(limit=100, offset=0, fields=None, filter=None, sort=None, user_id='<user_id> if needed')

# delete site block
client.delete_site_block(id=123, user_id='<user_id> if needed')

# update site block
client.update_site_block(id=123, name='update site block name', user_id='<user_id> if needed')
```

### Virtual Numbers
doc - <a href='https://www.comagic.ru/support/api/data-api/VirtualNumbers/'>Вирутальные номера</a>
```python
# get virtual numbers
virtual_numbers = client.get_virtual_numbers(limit=100, offset=0, fields=None, filter=None, sort=None,
user_id='<user_id> if needed')

# get available numbers
available_virtual_numbers = client.available_virtual_numbers(limit=100, offset=0, fields=None, filter=None, sort=None,
user_id='<user_id> if needed')

# enable virtual number
client.enable_virtual_number('793799992', user_id='<user_id> if needed')

# disable virtual number
client.disable_virtual_number('793799992', user_id='<user_id> if needed')
```

### Account
doc - <a href='https://www.comagic.ru/support/api/data-api/Account/'>Аккаунт</a>
```python
acc = client.get_account()
```

### Sip lines
doc <a href='https://www.comagic.ru/support/api/data-api/SipLines/'>Сип</a>
```python
# get sip virtual numbers
sip_virtual_numbers = client.get_sip_line_virtual_numbers(limit=100, offset=0, fields=None, filter=None, sort=None,
user_id='<user_id> if needed')

# create sip line
sip_line = client.create_sip_line(employee_id=2310, virtual_phone_number='793799992', user_id='<user_id> if needed')

# update sip line
updated_sip_line = client.update_sip_line(
employee_id=2310,
virtual_phone_number='793799992',
billing_state='manual_lock', # or active
channels_count=23,
user_id='<user_id> if needed'
)

# delete sip line
client.delete_sip_line(id=111, user_id='<user_id> if needed')

# get sip lines
sip_lines = client.get_sip_lines(limit=100, offset=0, fields=None, filter=None, sort=None,
user_id='<user_id> if needed')

# generate new password for sip line
password = client.update_sip_line_password(id=111, user_id='<user_id> if needed')
```

### Scenarios
doc - <a href='https://www.comagic.ru/support/api/data-api/Scenarios/'>Сценарии<a>
```python
# get scenarios
scenarios = client.get_scenarios(limit=100, offset=0, fields=None, filter=None, sort=None,user_id='<user_id> if needed')
```

### MediaFiles
doc - <a href='https://www.comagic.ru/support/api/data-api/UserMedia/'>Медиафайлы<a>
```python
media_files = client.get_media_files(limit=100, offset=0, fields=None, filter=None, sort=None,
user_id='<user_id> if needed')
```

### Campaigns
doc - <a href='https://www.comagic.ru/support/api/data-api/Campaigns/'>Рекламные кампании<a>
```python
# get campaigns
campaigns = client.get_campaigns(limit=100, offset=0, fields=None, filter=None, sort=None,
user_id='<user_id> if needed')

# delete campaign
client.delete_campaign(id=222, user_id='<user_id> if needed')

# get available number
numbers = client.get_campaign_available_phone_numbers(limit=100, offset=0, fields=None, filter=None, sort=None,
user_id='<user_id> if needed')

# get redirection numbers
redirection_numbers = client.get_campaign_available_redirection_phone_numbers(limit=100, offset=0, fields=None,
filter=None, sort=None,
user_id='<user_id> if needed')

# create campaign
campaign = client.create_campaign(name='test_campaign', site_id=123, status='active', user_id='<user_id> if needed')

# update campaign
updated_campaign = client.update_campaign(id=12, status='inactive')

# get campaign weights
campaign_weights = client.get_campaign_parameter_weights(limit=100, offset=0, fields=None,
filter=None, sort=None,
user_id='<user_id> if needed')

# update campaign weights
client.update_campaign_parameter_weights(site_id=123, entrance_page=99, user_id='<user_id> if needed')
```

### Tags
doc - <a href='https://www.comagic.ru/support/api/data-api/Tags/'>Теги<a>
```python
# create tag
tag = client.create_tag(name='test tag', user_id='<user_id> if needed')

# update tag
updated_tag = client.update_tag(id=1, name='updated', user_id='<user_id> if needed')

# delete tag
client.delete_tag(id=1, user_id='<user_id> if needed')

# get tags
tags = client.get_tags(limit=100, offset=0, fields=None,
filter=None, sort=None,
user_id='<user_id> if needed')
```
### Employees
doc - <a href='https://www.comagic.ru/support/api/data-api/Employees/'>Сотрудники<a>
```python
# get employees
employees = client.get_employees(limit=100, offset=0, fields=None,
filter=None, sort=None,
user_id='<user_id> if needed')

# create employee
client.create_employee(last_name='sidorov', phone_numbers=['79024256464'], user_id='<user_id> if needed')

# delete employee
client.delete_employee(id=11111, user_id='<user_id> if needed')

# update employee
client.update_employee(id=1, last_name='ivanov', user_id='<user_id> if needed')

# create employees group
client.create_employees_group(name='managers', members=['1'], user_id='<user_id> if needed')

# delete employee group
client.delete_employees_group(id=1, user_id='<user_id> if needed')

# update employee group
client.update_employees_group(id=1, name='developers')

# get employees groups
employees_groups = client.get_employees_groups(limit=100, offset=0, fields=None,
filter=None, sort=None,
user_id='<user_id> if needed')
```

### Contacts
doc - <a href='https://www.comagic.ru/support/api/data-api/Contacts/'>Адресная книга<a>
```python
# get contacts
contacts = client.get_contacts(limit=100, offset=0, fields=None,
filter=None, sort=None,
user_id='<user_id> if needed')

# delete contact
client.delete_contact(id=1, user_id='<user_id> if needed')

# create contact
contact = client.create_contact(last_name='ivanov', phone_numbers=['793799992'], user_id='<user_id> if needed')

# update contact
updated_contact = client.update_contact(id=1, last_name='ivanov', phone_numbers=['793799991'],
user_id='<user_id> if needed')

# create contact group
group = client.create_contact_group(name='test', user_id='<user_id> if needed')

# delete contact group
client.delete_contact_group(id=1, user_id='<user_id> if needed')

# get contact groups
groups = client.get_contact_groups(limit=100, offset=0, fields=None,
filter=None, sort=None,
user_id='<user_id> if needed')

# get contact organization
orgs = client.get_contact_organizations(limit=100, offset=0, fields=None,
filter=None, sort=None,
user_id='<user_id> if needed')

# create contact organization
client.create_contact_organization(name='test', user_id='<user_id> if needed')

# update contact organization
client.update_contact_organization(id=1, name='test', user_id='<user_id> if needed')

# delete contact organization
client.delete_contact_organization(id=1, user_id='<user_id> if needed')
```

### Schedules
doc - <a href='https://www.comagic.ru/support/api/data-api/Contacts/'>Графики активности<a>
```python
# get schedules
schedules = client.get_schedules(limit=100, offset=0, fields=None,
filter=None, sort=None,
user_id='<user_id> if needed')

# create schedule
client.create_schedule(name='first', user_id='<user_id> if needed')

# delete schedule
client.delete_schedule(id=1)

# update schedule
client.update_schedule(id=1, name='erste')
```

# Reports
doc - <a href='https://www.comagic.ru/support/api/data-api/Reports/'>Отчеты<a>
```python
from datetime import datetime, timedelta
date_from = datetime.now() - timedelta(days=1)
date_till = datetime.now()

# communication report
communication_report = client.get_communication_report(date_from=date_from, date_till=date_till, user_id='<user_id> if needed')

# calls report
calls_report = client.get_calls_report(date_from=date_from, date_till=date_till, user_id='<user_id> if needed')

# call legs report
call_legs_report = client.get_call_legs_report(date_from=date_from, date_till=date_till, user_id='<user_id> if needed')

# goals report
goals_report = client.get_goals_report(date_from=date_from, date_till=date_till, user_id='<user_id> if needed')

# chats report
chats_report = client.get_chats_report(date_from=date_from, date_till=date_till, user_id='<user_id> if needed')

# chat messages report
messages = client.get_chat_messages_report(chat_id=1, user_id='<user_id> if needed')

# offline messages report
offline_messages = client.get_offline_messages_report(date_from=date_from, date_till=date_till, user_id='<user_id> if needed')

# visitor sessions report
visitor_sessions_report = client.get_visitor_sessions_report(date_from=date_from, date_till=date_till, user_id='<user_id> if needed')

# financial call legs report
financial_call_legs_report = client.get_financial_call_legs_report(date_from=date_from, date_till=date_till, user_id='<user_id> if needed')
```

### Campaign daily stat
```python
from datetime import datetime, timedelta
date_from = datetime.now() - timedelta(days=1)
date_till = datetime.now()
campaign_daily_stat = client.get_campaign_daily_stat(date_from=date_from, date_till=date_till, user_id='<user_id> if needed')
```