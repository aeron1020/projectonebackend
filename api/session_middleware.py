from django.utils.deprecation import MiddlewareMixin

class EnsureSessionMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not request.session.session_key:
            request.session.create()
            print(f"Creating session key: {request.session.session_key}")
        else:
            print(f"Existing session key: {request.session.session_key}")
