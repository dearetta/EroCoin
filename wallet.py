from ecdsa import SigningKey, NIST256p
import os.path

class Wallet:
    def __init__(self):
        self.private = None
        self.private_hex = ""
        self.public = None
        self.public_hex = ""

    def generate_pairs(self):
        if os.path.isfile('key.dat'):
            file = open("key.dat", "rb")
            pv_key = SigningKey.from_string(file.readline(), curve=NIST256p)
            pb_key = pv_key.get_verifying_key()
            file.close()
            pv_string = pv_key.to_string()
            pb_string = pb_key.to_string()
            self.private = pv_string
            self.private_hex = pv_string.hex()
            self.public = pb_string
            self.public_hex = pb_string.hex()
            return pv_string.hex(), pb_string.hex()
        else:
            pv_key = SigningKey.generate(curve=NIST256p)
            pv_string = pv_key.to_string()
            pb_key = pv_key.get_verifying_key()
            pb_string = pb_key.to_string()
            file = open("key.dat", "wb")
            file.write(pv_string)
            file.close
            self.private = pv_string
            self.private_hex = pv_string.hex()
            self.public = pb_string
            self.public_hex = pb_string.hex()
            return pv_string.hex(), pb_string.hex()


    def get_balance(self):
        pass
