from typing import TYPE_CHECKING, Optional
from urllib.parse import parse_qsl

import pytz
from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin

from main.services import RemoteUser, ChannelCookie

User = get_user_model()

if TYPE_CHECKING:
    from django.http import HttpRequest


class HealthCheckMiddleware(MiddlewareMixin):
    def process_request(self, request: 'HttpRequest') -> Optional[HttpResponse]:
        if request.META['PATH_INFO'] == settings.HEALTH_CHECK_URL:
            return HttpResponse('pong')


class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: 'HttpRequest'):
        if tzname := request.COOKIES.get(getattr(settings, 'TIMEZONE_COOKIE_NAME', 'timezone')):
            timezone.activate(pytz.timezone(tzname))
        else:
            timezone.deactivate()
        return self.get_response(request)


class RemoteUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: 'HttpRequest'):
        request.remote_user = None
        if request.user.is_authenticated:
            request.remote_user = RemoteUser(id=request.user.pk, session=request.session.session_key)
        if user_id := request.headers.get('Remote-User'):
            request.remote_user = RemoteUser(id=int(user_id), session=request.session.session_key)
        return self.get_response(request)


class ChannelCookieMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: 'HttpRequest'):
        channel_cookie = request.COOKIES.get('reg_country')
        if not channel_cookie:
            return self.get_response(request)
        channel_model_dict = dict(parse_qsl(channel_cookie))
        request.channel = ChannelCookie(**channel_model_dict)
        return self.get_response(request)
