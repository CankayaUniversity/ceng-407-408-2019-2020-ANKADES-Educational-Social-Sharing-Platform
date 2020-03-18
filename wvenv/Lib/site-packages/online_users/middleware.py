from django.utils.deprecation import MiddlewareMixin

from online_users.models import OnlineUserActivity


class OnlineNowMiddleware(MiddlewareMixin):
    """Updates the OnlineUserActivity database whenever an authenticated user makes an HTTP request."""

    # def __init__(self, get_response):
    #     self.get_response = get_response
    #     # One-time configuration and initialization.
    #
    # def __call__(self, request):
    #     # Code to be executed for each request before
    #     # the view (and later middleware) are called.
    #
    #     response = self.get_response(request)
    #
    #     # Code to be executed for each request/response after
    #     # the view is called.
    #
    #     return response

    @staticmethod
    def process_request(request):
        user = request.user
        if not user.is_authenticated:
            return

        OnlineUserActivity.update_user_activity(user)
