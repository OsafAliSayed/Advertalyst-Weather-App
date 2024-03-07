import jwt
from django.http import JsonResponse
from django.conf import settings
from django.contrib.auth import get_user_model

class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # if url is login or register, pass
        if request.path == '/auth/jwt':
            return self.get_response(request)
        
        header = request.META.get('HTTP_AUTHORIZATION')

        if header is None:
            return JsonResponse({'error': 'No token provided'}, status=403)
        
        
        if header is not None:
            token = header.split(' ')[1]
            print(token)
            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
                print(payload)
                user = get_user_model().objects.get(id=payload['user_id'])
                request.user = user
            except jwt.ExpiredSignatureError:
                return JsonResponse({'error': 'Token expired'}, status=403)
            except (jwt.DecodeError, get_user_model().DoesNotExist):
                return JsonResponse({'error': 'Invalid token'}, status=403)

        response = self.get_response(request)
        return response