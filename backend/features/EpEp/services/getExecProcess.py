import requests
from config.paths import EpEpPaths
from models.getExecProcessById import GetExecProcessByIdResponse
from models.auth import Auth


def get_exec_process_by_id(id: str) -> GetExecProcessByIdResponse:
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {Auth().token}",
    }
    body = f'"{id}"'
    response = requests.post(EpEpPaths.GetExecProcessById, headers=headers, data=body)
    response.raise_for_status()

    return GetExecProcessByIdResponse.model_validate(response.json())
