from dotenv import find_dotenv, load_dotenv

from models.auth import Auth
from services.getAuth import get_auth_token

load_dotenv(find_dotenv())

try:
    auth_response = get_auth_token()
    Auth(auth_response["token"], auth_response["expiresIn"])
    print(Auth())
except Exception as e:
    print("Error:", e)
