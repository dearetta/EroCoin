from time import time

class Robot:
    def __init__(self, n, c, w):
        self.name = n
        self.color = c
        self.weight = w

    def introduce_self(self):
        print("My name is " + self.name)


# Same class method but with decorator More info: https://docs.python.org/3/library/functions.html#property
class Person:
    def __init__(self):
        self._name = ""
        self._personality = ""
        self._isSitting = False

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, val):
        # Decorator is useful when you want to insert a command when setting an attr
        print("Hello my name is " + val + " and I am " + self._personality)
        self._name = val

    # Notice how you can set _personality without having to add a setter/getter decorator?

    @property
    def isSitting(self):
        return self._isSitting

    @isSitting.setter
    def isSitting(self, val):
        self._isSitting = val

    def sit_down(self):
        self._isSitting = True
        print(self.name + " is now sitting")


r1 = Robot("Tom", "red", 30)
r2 = Robot("Jerry", "blue", 40)

# Declare attributes for 'Person' object
p1 = Person()
p1._personality = "Gay"
p1.name = "Astolfo"
p1.isSitting = False
p2 = Person()
p2._personality = "Useless"
p2.name = "Aqua"
p2.isSitting = True

p1.robot_owned = r2
p2.robot_owned = r1

print(p2.name + "'s robot is " + str(p2.robot_owned.weight) + " unit heavy")
p1.sit_down()
print("Is " + p1.name + " sitting? " + str(p1.isSitting))

# new-style class in Python3 testing.
# For details look here https://stackoverflow.com/questions/7375595/class-with-object-as-a-parameter
print(type(r2))
print(time())

apple = "apple"
test = str(''.join(format(ord(x), 'b') for x in apple))
print(type(test))
print(test)

import hashlib
import json

def generate_hash2(secret, param_str, param_dict):
    dk = hashlib.sha256()
    bsecret = str(secret).encode('utf-8')
    bparam_str = param_str.encode('utf-8')
    bparam_dict = json.dumps(param_dict).encode('utf-8')
    dk.update(bsecret)
    dk.update(bparam_str)
    dk.update(bparam_dict)
    return dk.hexdigest()


print(generate_hash2(2, "pie", {"apple": 2, "pie": 1}))

from ecdsa import SigningKey, NIST256p
from hashlib import sha256
import ecdsa

pv_key = SigningKey.generate(curve=NIST256p)
pv_string = pv_key.to_string().hex()
pb_key = pv_key.get_verifying_key()
pb_string = pb_key.to_string().hex()
print(pv_string, pb_string)
print(len("98cedbb266d9fc38e41a169362708e0509e06b3040a5dfff6e08196f8d9e49cebfb4f4cb12aa7ac34b19f3b29a17f4e5464873f151fd699c2524e0b7843eb383"))

import os.path

if os.path.isfile('key.dat'):
    file = open("key.dat", "rb")
    pv_key = SigningKey.from_string(file.readline(), curve=NIST256p)
    pb_key = pv_key.get_verifying_key()
    file.close()
    pv_string = pv_key.to_string()
    pb_string = pb_key.to_string()
    print("----------------\n")
    print(pv_string.hex(), pb_string.hex())
    print("------SIGN--------\n")
    sign = pv_key.sign(b"yeetusfeetus")
    print(sign.hex())
    assert pb_key.verify(sign, b"yeetusfeetus")
else:
    pv_key = SigningKey.generate(curve=NIST256p)
    pv_string = pv_key.to_string()
    pb_key = pv_key.get_verifying_key()
    pb_string = pb_key.to_string()
    file = open("key.dat", "wb")
    file.write(pv_string)
    file.close()
    print(pv_string.hex(), pb_string.hex())
    print("------SIGN--------\n")
    sign = pv_key.sign(b"yeetusfeetus")
    print(sign.hex())
    assert pb_key.verify(sign, b"yeetusfeetus")

print("--------------KEY VERIFICATION FROM EXISTING SIG------------")
message = "yeetusfeetus".encode()
public_key = "2ef97fbb2df87d662ce5b2ef13ecfe5023986063ecdb512692a128ca31f147e247735a639b15a9192ea4c429301b3a3aa097e13b34f3324b5e837ae79edad8b3"
verify_key = ecdsa.VerifyingKey.from_string(bytes.fromhex(public_key), curve=NIST256p)
if not verify_key.verify(bytes.fromhex(sign.hex()), message):
    print(False)
else:
    print("YEEY")