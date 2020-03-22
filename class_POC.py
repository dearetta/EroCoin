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

arr = [1,2,3,4,5,6,7,8]
foo = 3
print(arr[-1 - foo])
