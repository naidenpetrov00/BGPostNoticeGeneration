BASE_URL = "https://ecase-api-test.justice.bg/api/v2/"


class EpEpPaths:
    GetToken = f"{BASE_URL}Auth/GetToken"
    CaseById = f"{BASE_URL}Cases/{{caseId}}"  
