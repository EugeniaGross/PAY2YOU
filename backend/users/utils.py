from django.conf import settings


def get_full_url(path=None):
    url = settings.SWAGGER_SETTINGS['DEFAULT_API_URL']
    if settings.DEBUG and path:
        return f'http://127.0.0.1:8000/{path}'
    elif not settings.DEBUG and path:
        return f'{url}{path}'
    elif settings.DEBUG and not path:
        return 'http://127.0.0.1:8000/'
    elif not settings.DEBUG and not path:
        return f'{url}'
