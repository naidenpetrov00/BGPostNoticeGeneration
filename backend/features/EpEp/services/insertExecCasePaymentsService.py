import requests
from models.insertExecCasePayments import PaymentRequest
from config.paths import EpEpPaths
from models.getExecProcessById import GetExecProcessByIdResponse
from models.auth import Auth


def insert_exec_case_payments(
    exec_process: GetExecProcessByIdResponse,
    payment_type="Главница",
    side_name="ВАСИЛЕНА ДИМИТРОВА ПЕТРОВА",
    payment_date="2025-09-15T09:41:19.560Z",
    amount=20,
    currency_code="BGN",
):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {Auth().token}",
    }
    paymentRequest = populate_payment_request(
        exec_process, payment_type, side_name, payment_date, amount, currency_code
    )
    if paymentRequest is None:
        return
    body = paymentRequest.model_dump_json()
    response = requests.post(
        EpEpPaths.InsertExecCasePayment, headers=headers, data=body
    )
    response.raise_for_status()

    print(response.json())


def populate_payment_request(
    exec_process: GetExecProcessByIdResponse,
    payment_type: str,
    side_name: str,
    payment_date,
    amount,
    currency_code,
):
    obligation = next(
        filter(
            lambda o: o.obligationTypeName == payment_type, exec_process.obligationList
        ),
        None,
    )
    side = next(
        filter(lambda sl: sl.sideName == side_name, exec_process.sideList), None
    )
    if side is None or obligation is None:
        print(
            f"Could not match side:{side} or obligation: {obligation} for case: {exec_process.execCases[0].number}"
        )
    else:
        return PaymentRequest(
            execCaseGid=exec_process.execCases[0].gid,
            obligationGid=obligation.gid,
            debtorGid=side.gid,
            paymentDate=payment_date,
            amount=amount,
            currencyCode=currency_code,
        )
