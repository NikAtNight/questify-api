import logging
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model
import jwt
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

User = get_user_model()
logger = logging.getLogger(__name__)


class SupabaseTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None

        try:
            token_type, token = auth_header.split()
            if token_type.lower() != 'bearer':
                raise AuthenticationFailed('Invalid token type. Expected Bearer token.')

            decoded_token = self.verify_token(token)
            if not decoded_token:
                raise AuthenticationFailed('Invalid token.')

            try:
                user = User.objects.get(supabase_id=decoded_token['sub'])
            except ObjectDoesNotExist:
                raise AuthenticationFailed('User not found.')

            return (user, token)

        except ValueError:
            raise AuthenticationFailed('Invalid token header format.')
        except jwt.InvalidTokenError as e:
            raise AuthenticationFailed(f'Invalid token: {str(e)}')

    def verify_token(self, token):
        try:
            decoded_token = jwt.decode(
                token,
                settings.SUPABASE_JWT_SECRET,
                algorithms=settings.SUPABASE_JWT_ALGORITHMS,
                audience="authenticated",
                options={"verify_exp": True}
            )

            if decoded_token.get('iss') != settings.SUPABASE_JWT_ISSUER:
                raise jwt.InvalidTokenError('Invalid token issuer')

            return decoded_token
        except jwt.ExpiredSignatureError:
            logger.info('Token has expired.')
        except jwt.InvalidTokenError as e:
            logger.info(f'Invalid token error: {str(e)}')
        except Exception as e:
            logger.error(f'Unexpected error verifying token: {str(e)}')
        return None
