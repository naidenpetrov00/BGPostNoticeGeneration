from pandas import Series

import readData
from barcode import BarCode


class EnvelopeField:
    ENVELOPE_RECEIVER_GENERAL_INFO = "letter_general_info"
    BARCODE = "barcode"

    def getFieldValues(
        self, row: Series, barcode: BarCode
    ) -> dict[str, str | list[str] | tuple[str, str, float]]:
        reciever = row[readData.recieverProp]
        address = row[readData.adressProp]
        envelope_receiver_general_info = f"До: {reciever}\nAдрес: {address}"

        return {
            self.ENVELOPE_RECEIVER_GENERAL_INFO: envelope_receiver_general_info,
            self.BARCODE: barcode.get_full_barcode(),
        }
