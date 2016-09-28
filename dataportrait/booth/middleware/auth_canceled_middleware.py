from social.apps.django_app.middleware import SocialAuthExceptionMiddleware
from social.exceptions import AuthCanceled
from social import exceptions as social_exceptions

from django.shortcuts import redirect


class BoothAuthExceptionMiddleware(SocialAuthExceptionMiddleware):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def get_message(self, request, exception):
        return 'Auth Canceled'

    def get_redirect_uri(self, request, exception):
        if isinstance(exception, AuthCanceled):
            return '/auth-canceled'
        else:
            return super(BoothAuthExceptionMiddleware, self).get_redirect_uri(request, exception)

    def process_exception(self, request, exception):
        if hasattr(social_exceptions, exception.__class__.__name__):
            return redirect(self.get_redirect_uri(request, exception))
        else:
            raise exception