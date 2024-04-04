from drf_yasg import openapi
from rest_framework import status

response_schema_dict = {
    "200": openapi.Response(
        description="OK",
        examples={
            "application/json": {
                "message": "Оплата прошла",
            }
        }
    ),
    "400": openapi.Response(
        description="BAD REQUEST",
        examples={
            "application/json": {
                "message": "Оплата не прошла",
            }
        }
    ),
}

response_schema_dict_cashback = {
    "200": openapi.Response(
        description="OK",
        examples={
            "application/json": {
                "message": "Кэшбек начислен",
            }
        }
    ),
    "400": openapi.Response(
        description="BAD REQUEST",
        examples={
            "application/json": {
                "message": "Кэшбек не зачислен",
            }
        }
    ),
}
