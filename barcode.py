import os
import string



class BarCode:

    def _int_to_base36(self, num, width=6):
        alphabet = string.digits + string.ascii_uppercase
        base = len(alphabet)
        chars = []
        while num > 0:
            num, rem = divmod(num, base)
            chars.append(alphabet[rem])
        result = "".join(reversed(chars)).rjust(width, "0")
        return result

    def _generate_unique_number(self):
        filepath = "./config/last_number.txt"
        if os.path.exists(filepath):
            with open(filepath, "r") as f:
                last_number = int(f.read().strip())
        else:
            last_number = 0

        new_number = last_number + 1
        unique_code = self._int_to_base36(new_number)

        with open(filepath, "w") as f:
            f.write(str(new_number))

        return str(unique_code)
        # return str(new_number).zfill(6)

    def _calculate_controle_number(self):
        return self._char_to_code(self._get_barcode_for_control_number())

    def _char_to_code(self, text):
        result = 0
        text = text.upper()
        for char in text:
            if char.isdigit():
                result += int(char)
            elif "A" <= char <= "Z":
                result += ord(char) - ord("A") + 10
            else:
                raise ValueError(f"Invalid character: {char}")
        remainder = result % 36
        alphabet = string.digits + string.ascii_uppercase
        return alphabet[remainder]


    def _get_barcode_for_control_number(self):
        return f"{self.post_id}{self.client_id}{self.unique_number}"

    def __init__(self):
        self.post_id = "PS"
        self.client_id = "CHSI"
        self.unique_number = self._generate_unique_number()
        self.control_number = self._calculate_controle_number()

    def get_full_barcode(self):
        return (
            f"*{self.post_id}{self.client_id}{self.unique_number}{self.control_number}*"
        )
    
    def get_barcode_text(self):
        return (
            f"{self.post_id}{self.client_id}{self.unique_number}{self.control_number}"
        )
