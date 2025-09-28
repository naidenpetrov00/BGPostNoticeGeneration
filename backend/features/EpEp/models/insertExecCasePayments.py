from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel


class PaymentRequest(BaseModel):
    execCaseGid: UUID
    obligationGid: UUID
    debtorGid: UUID
    paymentDate: datetime
    amount: float
    currencyCode: str
    description: Optional[str] = None
