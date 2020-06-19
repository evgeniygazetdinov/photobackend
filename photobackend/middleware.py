from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from django.utils.timezone import now
from userapp.models import PhotoUser

class SetLastVisitMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            # Update last visit time after request finished processing.
            pass
        return None


class CurrentUserMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.session['cur_user'] = request.user
        return None