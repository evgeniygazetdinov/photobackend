from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin



class CurrentUserMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.session['cur_user'] = request.user
        return None