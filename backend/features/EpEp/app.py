from dotenv import find_dotenv, load_dotenv

from services.insertExecCasePaymentsService import (
    insert_exec_case_payments,
)
from services.getExecProcess import get_exec_process_by_id
from models.auth import Auth
from services.getAuth import get_auth_token

load_dotenv(find_dotenv())

try:
    auth_response = get_auth_token()
    Auth(auth_response["token"], auth_response["expiresIn"])
except Exception as e:
    print("Error:", e)

try:
    exec_process = get_exec_process_by_id("9ecf9ff7-12f4-4abb-827a-511543314cfe")
    insert_exec_case_payments(exec_process)
except Exception as e:
    print("Error:", e)
