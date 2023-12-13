import jwt
import datetime
import pytz
from prettyconf import config


class JWT:

    @staticmethod
    def generate(username):

        local_timezone = pytz.timezone("America/Sao_Paulo")
        current_time = datetime.datetime.now(local_timezone)

        payload = {
            "username": username,
            "iat": current_time,
            "exp": current_time + datetime.timedelta(minutes=int(config('JWT_DURATION'))),
            "env": config('ENV'),
            "application": "WaveMessage"
        }

        secret_key = config("JWT_SECRET_KEY")
        token = jwt.encode(payload, secret_key, algorithm="HS256")

        return token

    @staticmethod
    def validate(token):
        secret_key = config("JWT_SECRET_KEY")
        try:
            jwt.decode(token, secret_key, algorithms=["HS256"])
            return True
        except jwt.ExpiredSignatureError:
            print("Token expirado")
            return False
        except jwt.InvalidTokenError:
            print("Token inválido")
            return False

    @staticmethod
    def token_username(token):
        secret_key = config("JWT_SECRET_KEY")
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])

        return payload['username']
