from django.http import Http404
from django.test import TestCase
from django.test.client import RequestFactory
from django.urls import reverse

from misago.cache.versions import get_cache_versions
from misago.conf.dynamicsettings import DynamicSettings
from misago.core.middleware import ExceptionHandlerMiddleware
from misago.users.models import AnonymousUser


class ExceptionHandlerMiddlewareTests(TestCase):
    def setUp(self):
        request = RequestFactory().get(reverse('misago:index'))
        request.user = AnonymousUser()
        request.cache_versions = get_cache_versions()
        request.settings = DynamicSettings(request.cache_versions)
        request.include_frontend_context = True
        request.frontend_context = {}

        self.request = request

    def test_middleware_returns_response_for_supported_exception(self):
        """Middleware returns HttpResponse for supported exception"""
        exception = Http404()
        middleware = ExceptionHandlerMiddleware()

        self.assertTrue(middleware.process_exception(self.request, exception))

    def test_middleware_returns_none_for_non_supported_exception(self):
        """Middleware returns None for non-supported exception"""
        exception = TypeError()
        middleware = ExceptionHandlerMiddleware()

        self.assertFalse(middleware.process_exception(self.request, exception))
