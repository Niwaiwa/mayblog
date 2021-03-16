from dotenv import load_dotenv
from pathlib import Path  # Python 3.6+ only
import os


env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
env = os.getenv('FLASK_ENV')
debug = bool(os.getenv('FLASK_DEBUG', False))
secret_key = os.getenv('SECRET_KEY', "secret!")
domain = os.getenv('DOMAIN')

username = os.getenv('MYSQL_USERNAME', 'root')
password = os.getenv('MYSQL_PASSWORD', 'password')
host = os.getenv('MYSQL_HOST', 'localhost')
port = int(os.getenv('MYSQL_PORT', 3306))
database = os.getenv('MYSQL_DATABASE', 'test')

login_expire_sec = int(os.getenv('LOGIN_EXPIRE_SEC', 3600))

except_auth_path = [
    '/',
    '/index',
    '/auth/register',
    '/auth/login',
]