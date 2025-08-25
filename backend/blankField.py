from pandas import Series
from barcode import BarCode
import readData


sender_name = ""
sender_address = ""
sender_city = ""


class BlankFields:
    RECEIVER_GENERAL_INFO = "reciever_genral_info"
    ADDRESS = "address"
    CITY = "city"
    SENDER = "sender"
    SENDER_ADDRESS = "sender_address"
    SENDER_CITY = "sender_city"
    DOCUMENT_NUMBER = "document_number"
    BARCODE = "barcode"

    def getFieldValues(self, row: Series, barcode: BarCode, prev_row_doc_number=None):
        current_doc = row[readData.documentNumber]
        out_date = row[readData.outDate].split("/")[-1]
        document_number = f"*{out_date}-{current_doc}*"

        if prev_row_doc_number is None:
            doc_info = f"{current_doc}"
        else:
            doc_info = f"{prev_row_doc_number}, {current_doc}"
        generalInfo = f"{row[readData.recieverProp]} \nУдостоверявам, че получих документ(и) с изх№: {doc_info} ИД {row[readData.caseNumberProp]}"

        return {
            self.RECEIVER_GENERAL_INFO: generalInfo,
            self.ADDRESS: row[readData.adressProp],
            self.SENDER: sender_name,
            self.SENDER_ADDRESS: sender_address,
            self.SENDER_CITY: sender_city,
            self.DOCUMENT_NUMBER: document_number,
            self.BARCODE: barcode.get_full_barcode(),
        }
