from drf_yasg import openapi
from rest_framework import status

response_schema_dict_service_detail = {
    "200": openapi.Response(
        description="OK",
        examples={
            "application/json": {
                "id": "61f0c404-5cb3-11e7-907b-a6006ad3dba0",
                "name": "Okko",
                "full_name": "Okko: фильмы",
                "short_description": "Фильмы и сериалы",
                "cashback": 5,
                "logo": "https://www.example.com/media/123.jpg",
                "description": "Большое количество фильмов",
                "url": "https://okko.tv/"
            }
        }
    ),
    "401": openapi.Response(
        description="UNAUTHORIZED",
    ),
    "404": openapi.Response(
        description="NOT FOUND",
    )
}
response_schema_dict_services_list = {
    "200": openapi.Response(
        description="OK",
        examples={
            "application/json": {
                "data": [
                    {
                        "id": "61f0c404-5cb3-11e7-907b-a6006ad3dba0",
                        "logo": "https://www.example.com/123.jpg",
                        "name": "Okko",
                        "cashback": 5
                    }
                ],
                "next": "https://www.example.com/services/?skip=5&top=0",
                "previous": "https://www.example.com/services/?skip=5&top=6"
            }
        }
    ),
    "401": openapi.Response(
        description="UNAUTHORIZED",
    )
}
response_schema_dict_image_categories_list = {
    "200": openapi.Response(
        description="OK",
        examples={
            "application/json": {
                "data": [
                    {
                        "id": "61f0c404-5cb3-11e7-907b-a6006ad3dba0",
                        "name": "Популярные"
                    }
                ],
                "next": ("https://www.example.com/services/"
                         "61f0c404-5cb3-11e7-907b-a6006ad3dba0/"
                         "image-categories/?skip=5&top=0"),
                "previous": ("https://www.example.com/services/"
                             "61f0c404-5cb3-11e7-907b-a6006ad3dba0/"
                             "image-categories/?skip=5&top=6")
            }
        }
    ),
    "401": openapi.Response(
        description="UNAUTHORIZED",
    ),
    "404": openapi.Response(
        description="NOT FOUND",
    )
}
response_schema_dict_service_image_categories_list = {
    "200": openapi.Response(
        description="OK",
        examples={
            "application/json": {
                "data": [
                    {
                        "id": "61f0c404-5cb3-11e7-907b-a6006ad3dba0",
                        "title": "Популярные",
                        "image": "https://www.example.com/madia/23.jpg"
                    }
                ],
                "next": ("https://www.example.com/services/"
                         "61f0c404-5cb3-11e7-907b-a6006ad3dba0/"
                         "image-categories/71f0c404-5cb3-11e7-907b-a6006ad3dba0/"
                         "images/?skip=5&top=0"),
                "previous": ("https://www.example.com/services/"
                             "61f0c404-5cb3-11e7-907b-a6006ad3dba0/image-categories/"
                             "71f0c404-5cb3-11e7-907b-a6006ad3dba0/"
                             "images/?skip=5&top=6")
            }
        }
    ),
    "401": openapi.Response(
        description="UNAUTHORIZED",
    ),
    "404": openapi.Response(
        description="NOT FOUND",
    )
}
response_schema_dict_popular_services_list = {
    "200": openapi.Response(
        description="OK",
        examples={
            "application/json": {
                "data": [
                    {
                        "id": "61f0c404-5cb3-11e7-907b-a6006ad3dba0",
                        "logo": "https://www.example.com/123.jpg",
                        "cashback": 5
                    }
                ],
                "next": ("https://www.example.com/"
                         "popular-services/?skip=5&top=0"),
                "previous": ("https://www.example.com/popular-services/"
                             "?skip=5&top=6")
            }
        }
    ),
    "401": openapi.Response(
        description="UNAUTHORIZED",
    )
}
response_schema_dict_tariffs_list = {
    "200": openapi.Response(
        description="OK",
        examples={
            "application/json": {
                "data": [
                    {
                        "id": "61f0c404-5cb3-11e7-907b-a6006ad3dba0",
                        "name": "Прайм",
                        "description": "5000 фильмов и сериалов"
                    }
                ],
                "next": ("https://www.example.com/services/"
                         "61f0c404-5cb3-11e7-907b-a6006ad3dba0/"
                         "tariffs/?skip=5&top=0"),
                "previous": ("https://www.example.com/services/"
                             "61f0c404-5cb3-11e7-907b-a6006ad3dba0/"
                             "tariffs/?skip=5&top=6")
            }
        }
    ),
    "401": openapi.Response(
        description="UNAUTHORIZED",
    ),
    "404": openapi.Response(
        description="NOT FOUND",
    )
}
response_schema_dict_tariff_detail = {
    "200": openapi.Response(
        description="OK",
        examples={
            "application/json": {
                "data": [
                    {
                        "id": "61f0c404-5cb3-11e7-907b-a6006ad3dba0",
                        "name": "Прайм",
                        "description": "5000 фильмов и сериалов",
                        "condition": {
                            "count": 1,
                            "period": "Месяц",
                            "price": 199
                        },
                        "special_condition": {
                            "count": 1,
                            "period": "Месяц",
                            "price": 99
                        },
                        "trial_period": {
                            "count": 30,
                            "period": "Дней",
                            "price": 0
                        }
                    }
                ],
                "next": ("https://www.example.com/services/"
                         "61f0c404-5cb3-11e7-907b-a6006ad3dba0/tariffs/"
                         "61f0c404-5cb3-11e7-907b-a6006ad3dba0/?skip=5&top=0"),
                "previous": ("https://www.example.com/services/"
                             "61f0c404-5cb3-11e7-907b-a6006ad3dba0/tariffs/"
                             "61f0c404-5cb3-11e7-907b-a6006ad3dba0/?skip=5&top=6")
            }
        }
    ),
    "401": openapi.Response(
        description="UNAUTHORIZED",
    ),
    "404": openapi.Response(
        description="NOT FOUND",
    )
}