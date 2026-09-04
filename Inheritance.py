#This program demonstrates the concept of inheritance in Python.

class Animal:
    def speak(self):
        print("Animals make sounds.")
class Dog(Animal):
    def sound(self):
        print("Dogs bark.")

animal1 = Dog()
animal1.sound()  # Output: Dogs bark.
animal1.speak()  # Output: Animals make sounds.
