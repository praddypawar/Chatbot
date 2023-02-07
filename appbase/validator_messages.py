from django.core.validators import RegexValidator



zip_validator = RegexValidator(r'^[0-9]{6,10}$')
phone_validator = RegexValidator(r'^[0-9]{10,15}$')
po_fax_validator = RegexValidator(r'^[0-9]{6,12}$')
ext_validator = RegexValidator(r'^[0-9]{3,15}$')
warehouse_name = RegexValidator(r'^[a-zA-Z\- ]+$')
email_validator = RegexValidator(r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$', code='Invalid Email', message='Invalid Email')
email_validator2 = RegexValidator(r'^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$', code='Invalid Email', message='Invalid Email')
url_validator = RegexValidator( r'^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$/',message='Not a valid URL')