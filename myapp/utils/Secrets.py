import string
import secrets
from conf import settings


LETTERS = string.ascii_letters
NUMBERS = string.digits  
PUNCTUATION = string.punctuation    

class Secrets():

    @staticmethod
    def generate_password(length=10, letters=True, digits=True, punctuation=False):
        alphabet = ""
        if letters:
            alphabet = string.ascii_letters
        if digits:
            alphabet += string.digits
        if punctuation:
            alphabet += string.punctuation
        if alphabet:
            return ''.join(secrets.choice(alphabet) for i in range(length))
        return ""
    
    @staticmethod
    def generate_password_strong(length=10):
        alphabet = string.ascii_letters + string.digits
        while True:
            password = ''.join(secrets.choice(alphabet) for i in range(10))
            if (any(c.islower() for c in password)
                    and any(c.isupper() for c in password)
                    and any(c.isdigit() for c in password)):
                    # and sum(c.isdigit() for c in password) >= 3):
                break
        return

    @staticmethod
    def temporary_url():
        token = secrets.token_urlsafe()
        url = f'{settings.domain}/reset={token}'
        return url

    @staticmethod
    def generate_token_urlsafe(length=10):
        return secrets.token_urlsafe(length)

    @staticmethod
    def generate_token_hex(length=10):
        return secrets.token_hex(length)