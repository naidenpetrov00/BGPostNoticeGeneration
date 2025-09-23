from typing import List, Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel


class PaymentDto(BaseModel):
    gid: UUID
    obligationGid: UUID
    debtorGid: UUID
    paymentDate: Optional[datetime]  
    amount: float
    currencyCode: str
    description: str


class FileDto(BaseModel):
    gid: UUID
    fileType: int
    fileName: str
    fileTitle: str


class ExecCaseDto(BaseModel):
    gid: UUID
    number: str
    dateRegister: datetime
    userName: str
    stateCode: str
    stateName: str
    listDeliveryDate: Optional[datetime]  
    redirect427Date: Optional[datetime]  
    listTerminateDate: Optional[datetime]  
    caseTerminateDate: Optional[datetime]  
    payments: List[PaymentDto]
    files: List[FileDto]


class SideDto(BaseModel):
    gid: UUID
    subjectKind: int
    sideUic: Optional[str]  
    sideName: str
    sideRoleCode: str
    sideRoleName: str
    sideType: int
    addressTypeCode: str
    addressTypeName: str
    countryCode: str
    address: str


class ObligationDto(BaseModel):
    gid: UUID
    obligationTypeCode: str
    obligationTypeName: str
    beneficiaryGid: UUID
    amount: float
    currencyCode: str
    statutoryInterestDate: Optional[datetime]  
    description: Optional[str]  
    debtors: List[UUID]


class AccessDto(BaseModel):
    gid: UUID
    createDate: datetime
    accessKey: str
    creator: str
    userName: str
    isClaimed: bool
    isActive: bool
    canChange: bool
    dateClaimed: datetime


class CorrectionActDto(BaseModel):
    gid: UUID
    actKind: str
    actNumber: int
    actDate: datetime
    actFileId: UUID


class ClaimDocumentFileDto(BaseModel):
    gid: UUID
    fileType: int
    fileName: str
    fileTitle: str


class GetExecProcessByIdResponse(BaseModel):
    gid: UUID
    caseNumber: int
    caseYear: int
    caseKindName: str
    courtName: str
    actNumber: int
    actDate: datetime
    orderNumber: Optional[int]  
    orderDate: Optional[datetime]  
    execCases: List[ExecCaseDto]
    isExpired: bool
    caseGid: UUID
    actGid: UUID
    actFileId: UUID
    orderFileId: Optional[UUID]  
    hasCorrectedAct: bool
    jointDistribution: bool
    infoExpired: Optional[str]  
    sideList: List[SideDto]
    obligationList: List[ObligationDto]
    accessList: List[AccessDto]
    correctionActList: List[CorrectionActDto]
    claimDocumentFiles: List[ClaimDocumentFileDto]
