class Person:
    # Class variable
    species = "Human"

    def __init__(self, name, age):
        # Instance variables
        self.name = name
        self.age = age

    # =========================
    # INSTANCE METHOD
    # =========================
    def introduce(self):
        print(f"My name is {self.name} and I am {self.age} years old.")

    # =========================
    # CLASS METHOD
    # =========================
    @classmethod
    def show_species(cls):
        print(f"Species: {cls.species}")

    # =========================
    # STATIC METHOD
    # =========================
    @staticmethod
    def is_adult(age):
        return age >= 18


# Inheritance
class Student(Person):

    def __init__(self, name, age, university):
        # super() calls the parent class's __init__()
        super().__init__(name, age)

        self.university = university

    # Overriding the parent's instance method
    def introduce(self):

        # super() calls the parent's introduce() method
        super().introduce()

        print(f"I study at {self.university}.")


# =========================
# OBJECT CREATION
# =========================

student = Student("Umar", 20, "UMT")


# Instance method
student.introduce()


# Class method
Student.show_species()


# Static method
print(Student.is_adult(20))
print(Student.is_adult(15))