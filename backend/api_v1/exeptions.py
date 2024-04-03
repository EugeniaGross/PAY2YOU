from rest_framework.exceptions import APIException


class PaymentError(APIException):
    status_code = 400
    default_detail = 'Ошибка совершения платежа'
    default_code = 'payment_error'


class CashbackError(APIException):
    status_code = 400
    default_detail = 'Ошибка зачисления кэшбека'
    default_code = 'cashback_error'
