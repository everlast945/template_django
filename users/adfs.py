from jose import jwt, ExpiredSignatureError
from django.conf import settings

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated

from users.models import User


class AdfsValidateBase:
    CERT_KEY = settings.ADFS_CERT_KEY
    PUBLIC_KEYS = settings.ADFS_PUBLIC_KEYS
    ALGORITMS = ['RS256']

    @classmethod
    def get_valid_token(cls, token):
        """
        Получение расшифрованного валидного токена
        """
        token_headers = jwt.get_unverified_header(token)
        rsa_key = cls.get_rsa_key(token_headers)
        try:
            valid_token = jwt.decode(token, rsa_key, algorithms=cls.ALGORITMS, audience=settings.ADFS_AUDIENCE)
        except ExpiredSignatureError as ex:
            raise NotAuthenticated('Срок действия подписи истек')
        except Exception as ex:
            raise AuthenticationFailed()
        return valid_token

    @classmethod
    def get_rsa_key(cls, token_headers):
        """
        Получение публичного ключа для валидации
        """
        for key in cls.PUBLIC_KEYS["keys"]:
            if key[cls.CERT_KEY] == token_headers[cls.CERT_KEY]:
                return {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"]
                }


class AdfsAccessTokenValidate(AdfsValidateBase):
    """
    Валидация Access токена
    """
    pass


class AdfsAuth(BaseAuthentication):
    """
    Авторизация по токену ADFS
    """
    def authenticate(self, request):
        token = request.META.get('HTTP_AUTHORIZATION', b'')
        if not token or 'JWT ' not in token:
            return None
        valid_token = AdfsAccessTokenValidate.get_valid_token(token.replace('JWT ', ''))
        x5_email = valid_token[settings.ADFS_USERNAME_FIELD]
        # Получение/создание пользователя по логину в токене
        user, _ = User.create_x5_user(username=x5_email.split('@')[0], email=x5_email)
        # Привязка к пользователю профиля
        if not user.is_active:
            raise AuthenticationFailed('Пользователь не активен')
        return (user, None)

    def authenticate_header(self, request):
        return 'JWT realm=AdfsAuth'
