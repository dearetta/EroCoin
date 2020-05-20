from ecdsa import SigningKey, NIST256p
import os.path

class Wallet:
    def __init__(self):
        self.private = None  # private key on the form of hex
        self.private_decode = ""  # private key on the form of string (decoded hex)
        self.public = None  # public key on the form of hex
        self.public_decode = ""  # public key on the form of string (decoded hex)

    def generate_pairs(self):
        if os.path.isfile('key.dat'):  # if key.dat exist
            file = open("key.dat", "rb")  # open file read-only
            pv_key = SigningKey.from_string(file.readline(), curve=NIST256p)  # get private key from the file as an object
            pb_key = pv_key.get_verifying_key()  # generate public key from private key as an object
            file.close()  # close file
            pv_string = pv_key.to_string()  # change object type to string
            pb_string = pb_key.to_string()  # change object type to string
        else:
            pv_key = SigningKey.generate(curve=NIST256p)  # generate a new random private key
            pv_string = pv_key.to_string()  # change object type to string
            pb_key = pv_key.get_verifying_key()  # generate public key from private key as an object
            pb_string = pb_key.to_string()  # change object type to string
            file = open("key.dat", "wb")  # create new file called key.dat
            file.write(pv_string)  # write into key.dat
            file.close()  # close file
        self.private = pv_string
        self.private_decode = pv_string.hex()
        self.public = pb_string
        self.public_decode = pb_string.hex()
        return pv_string.hex(), pb_string.hex()


    def get_balance(self):
        pass
