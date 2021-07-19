from django.http import JsonResponse


class UserMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        print(exception.__class__.__name__)
        print(exception)
        return JsonResponse({'exception class': exception.__class__.__name__, 'exception message': str(exception)})
