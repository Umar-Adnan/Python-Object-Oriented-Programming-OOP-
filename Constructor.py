class Student:
    def __init__(self):
        self.name=input("Enter you name: ")
        self.age =int(input("Enter your age: "))
        print(f"\tStudent object s1 with name: {self.name}\n\tand age: {self.age} is created")  #message to indicate that the object has been created

s1=Student() # This line creates an instance of the Student class
