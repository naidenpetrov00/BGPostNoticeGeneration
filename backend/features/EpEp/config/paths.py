BASE_URL = "https://ecase-api-test.justice.bg/api/v2/"


class EpEpPaths:
    GetToken = f"{BASE_URL}Auth/GetToken"
    GetExecProcessById = f"{BASE_URL}ExecProcess/GetExecProcessById"
    InsertExecCasePayment = f"{BASE_URL}ExecProcess/InsertExecCasePayment"
    CaseById = f"{BASE_URL}Cases/{{caseId}}"
