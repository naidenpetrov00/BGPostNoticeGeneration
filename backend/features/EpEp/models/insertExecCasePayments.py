from typing import List, Optional
from uuid import UUID, uuid4
from datetime import datetime
from pydantic import BaseModel, Field


class PaymentRequest(BaseModel):
    execCaseGid: UUID
    obligationGid: UUID
    debtorGid: UUID
    paymentDate: datetime
    amount: float
    currencyCode: str
    description: Optional[str] = None
