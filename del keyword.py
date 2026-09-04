class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def display_info(self):
        print(f"Name: {self.name}, Age: {self.age}")

    s1 = Student("Alice", 20)
    del s1.age
    s1.display_info()  # This will raise an AttributeError since 'age' has been deleted.
    del s1  # This will delete the instance 's1' of the Student class.
    s1.display_info()  # This will raise a NameError since 's1' has been deleted.